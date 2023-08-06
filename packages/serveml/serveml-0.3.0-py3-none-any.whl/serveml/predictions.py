import logging

from abc import ABC, abstractmethod

import numpy as np
import pandas as pd

from serveml.inputs import BasicInput
from serveml.utils import pydantic_model_to_pandas, pandas_to_dict


class AbstractPrediction(ABC):
    """
    Abstract class to define methods called during predict
    """

    def __init__(self, model):
        self.model = model

    @abstractmethod
    def _transform_input(self, input):
        """
        Function called right after API call. It is supposed to transform
        <pydantic.BaseModel> object into the input data format needed to apply
        model
        """

    @staticmethod
    def _fetch_data(input: BasicInput):
        """
        Helper function in case we need additional data. In most of the cases,
        can be ignored
        """
        pass

    @staticmethod
    def _combine_fetched_data_with_input(fetched_data, transformed_input):
        return transformed_input

    @abstractmethod
    def _apply_model(self, transformed_input):
        """
        Function called to apply Machine Learning model to predict from the
        transformed input
        """

    @abstractmethod
    def _transform_output(self, output):
        """
        Function called right after applying model to input data. Supposed to
        transform the data that we got after the predict in order to
        """

    def predict(self, input, uuid):
        """
        Main function that will be used by all the childs to apply model.
        Here are the steps made :
            - Transform <pydantic.BaseModel> objet to target input object
            before applying model
            - Apply model
            - Transform output into more suitable format for an API
            - Add an uuid to the request to track request made
        """
        logging.debug(
            "Got input: {} for request_id: {}".format(input.dict(), uuid)
        )
        logging.info("Transforming input for request: {}".format(uuid))
        transformed_input = self._transform_input(input)
        logging.debug(
            "Input transformed to this: {}".format(transformed_input)
        )
        logging.info("Fetching data for request: {}".format(uuid))
        fetched_data = self._fetch_data(input)
        logging.debug("Fetched data: {}".format(fetched_data))
        logging.info(
            "Combining fetched data and input for request {}".format(uuid)
        )
        combined_data = self._combine_fetched_data_with_input(
            fetched_data, transformed_input
        )
        logging.debug("Combined data: {}".format(combined_data))
        logging.info("Applying input for request {}".format(uuid))
        output = self._apply_model(combined_data)
        logging.debug("Prediction output: {}".format(output))
        logging.info("Transforming output for request {}".format(uuid))
        transformed_output = self._transform_output(output)
        logging.debug("Transformed output: {}".format(transformed_output))
        transformed_output["request_id"] = uuid
        return transformed_output


class GenericPrediction(AbstractPrediction):
    """
    Implementation of <serveml.ml.model.AbstractModel> for scikit-learn
    """

    def _transform_input(self, input) -> pd.DataFrame:
        """
        Transforms <pydantic.BaseModel> object to <pandas.DataFrame>
        """
        return pydantic_model_to_pandas(input)

    def _apply_model(self, transformed_input: pd.DataFrame):
        """
        Applies the sklearn model to the <pandas.DataFrame>.
        Returns either one of these:
            - <pandas.DataFrame>
            - <pandas.Series>
            - <numpy.ndarray>
        """
        return self.model.predict(transformed_input)

    def _transform_output(self, output) -> dict:
        """
        Transforms output given by <serveml.ml.sklearn._apply_model> to
        prepare sending result with API.
        """
        if isinstance(output, np.ndarray):
            result = output.tolist()
        elif isinstance(output, pd.DataFrame):
            result = pandas_to_dict(output)
        elif isinstance(output, pd.Series):
            result = output.to_dict()
        else:
            result = None
        return {"result": result}
