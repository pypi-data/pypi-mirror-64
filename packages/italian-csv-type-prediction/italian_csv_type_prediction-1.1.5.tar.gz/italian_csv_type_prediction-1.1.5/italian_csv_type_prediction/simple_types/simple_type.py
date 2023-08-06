from typing import Dict


class SimpleTypePredictor:
    """
        A simple type predictor is a predictor that
        tries to guess the type of an object by only
        using the string properties.

        This type of predictor mainly tries to avoid
        false negatives.
    """
    
    def validate(self, candidate, **kwargs: Dict) -> bool:
        """Return boolean representing if type is identified.

        Parameters
        -----------------------------------
        candidate,
            The candidate to be identified.
        kwargs:Dict,
            Additional features to be considered.
        """
        raise NotImplementedError(
            "Method validate must be implemented in child class."
        )
