import enum
from typing import Dict
import asyncio
import concurrent.futures

from pyrit.models.prompt_request_piece import PromptRequestPiece
from pyrit.score import Score, Scorer
from pyrit.score.self_ask_category_scorer import SelfAskCategoryScorer


class MultiSelfAskCategoryScorer(Scorer):
    """
    A class that represents a multi-self-ask score for text classification and scoring.
    Given a list of SelfAskCategoryScorer, it will evaluate each one and return if any of them were true.
    """

    def __init__(self, scorers: list[SelfAskCategoryScorer]) -> None:
        """
        Initializes a new instance of the MultiSelfAskCategoryScorer class.

        Args:
            scorers (List[SelfAskCategoryScorer]): The list of scorers to evaluate.
        """
        self.scorer_type = "true_false"
        self._scorers = scorers

    async def score_async(self, request_response: PromptRequestPiece) -> list[Score]:
        """
        Scores the request response.

        Args:
            request_response (PromptRequestPiece): The request response to score.

        Returns:
            list[Score]: The scores.
        """
        scores = []
        for scorer in self._scorers:
            # REVIEW: It appears that although score_async returns a list, it looks like it always only returns one score. Just I loop through the list or just use [0]?
            scores.append((await scorer.score_async(request_response=request_response))[0])

        return scores
    
    def validate(self, request_response: PromptRequestPiece):
        pass