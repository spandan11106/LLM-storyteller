from typing import List, Optional
import random
from sentence_transformers import SentenceTransformer
from .llm_client import client
from . import config
import re


class PlayerAgent:
    """Simple planner for the AI Player.

    Behavior:
    - Ask the LLM for 3 candidate short actions (few-shot), given persona + retrieved context + goal.
    - Rank candidates by semantic similarity to retrieved context using SentenceTransformer.
    - Filter out obvious off-topic actions (must reference at least one recent entity or a plot keyword), resample up to N times.
    - Return a single concise action string.
    """

    def __init__(self, embedding_model: Optional[str] = None):
        self.embedding_model_name = embedding_model or config.EMBEDDING_MODEL
        self.embedder = SentenceTransformer(self.embedding_model_name)

    def _build_prompt(self, persona: str, goal: str, context: str, examples: List[str] = None) -> str:
        examples = examples or []
        ex_text = "\n".join(f"- {e}" for e in examples)
        prompt = (
            f"You are Valerius (player) persona: {persona}\n"
            f"Goal: {goal}\n"
            f"Context (use this to stay consistent):\n{context}\n"
            "Produce 3 short (one-sentence) in-character actions the player could take next, each on a separate line."
        )
        if ex_text:
            prompt += "\nExamples:\n" + ex_text
        return prompt

    def generate_candidates(self, persona: str, goal: str, context: str, n: int = 3) -> List[str]:
        prompt = self._build_prompt(persona, goal, context)
        try:
            resp = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model=config.LLM_MODEL)
            text = resp.choices[0].message.content
            # split into lines, keep up to n
            lines = [l.strip().lstrip('- ').strip() for l in text.splitlines() if l.strip()]
            return lines[:n] if lines else []
        except Exception:
            # fallback deterministic options
            return ["I ask a nearby NPC for information.", "I look around the room for clues.", "I wait and listen to the surroundings."][:n]

    def score_candidates(self, candidates: List[str], context: str) -> List[float]:
        if not candidates:
            return []
        try:
            emb_ctx = self.embedder.encode(context)
            embs = self.embedder.encode(candidates)
            import numpy as np
            scores = [float(np.dot(emb, emb_ctx) / ( (np.linalg.norm(emb)+1e-9)*(np.linalg.norm(emb_ctx)+1e-9) )) for emb in embs]
            return scores
        except Exception:
            # fallback equal scores
            return [1.0 for _ in candidates]

    def _relevance_filter(self, action: str, context: str, plot_point: Optional[str] = None) -> bool:
        # require action to mention at least one named entity from context or a plot keyword
        names = re.findall(r"\b[A-Z][a-zA-Z0-9_'\-]+\b", context)
        names = [n.split()[0] for n in names]
        lowered = action.lower()
        for n in names:
            if n.lower() in lowered:
                return True
        if plot_point:
            for token in re.sub(r'[_\-]+', ' ', plot_point).split():
                if token.lower() in lowered:
                    return True
        # otherwise allow safe actions that are neutral and short
        safe_patterns = [r"look", r"examine", r"ask", r"listen", r"wait", r"move", r"approach"]
        if any(re.search(p, lowered) for p in safe_patterns):
            return True
        return False

    def choose_action(self, persona: str, goal: str, context: str, plot_point: Optional[str] = None, temperature: float = 0.6) -> str:
        attempts = 0
        while attempts < 3:
            candidates = self.generate_candidates(persona, goal, context, n=3)
            if not candidates:
                attempts += 1
                continue
            scores = self.score_candidates(candidates, context)
            ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
            # pick best that passes relevance filter
            for cand, sc in ranked:
                if self._relevance_filter(cand, context, plot_point):
                    # optionally sample with softmax influenced by temperature
                    return cand
            # if none pass, try again
            attempts += 1
        # final fallback: return top ranked
        if candidates:
            return ranked[0][0]
        return "I look around carefully and decide my next move."
