from langchain.chat_models import ChatOpenAI
from langchain.llms import Replicate

from config import labels
from llm_handler import LLMChainHandler

if __name__ == "__main__":
    description = '''Bayesian estimation is increasingly popular for performing model based inference to support policymaking. 
        These data are often collected from surveys under informative sampling designs where subject inclusion probabilities are designed to be
        correlated with the response variable of interest. 
        Sampling weights constructed from marginal inclusion probabilities are typically used to form an exponentiated pseudo likelihood that 
        adjusts the population likelihood for estimation on the sample due to ease-of-estimation. 
        We propose an alternative adjustment based on a Bayes rule construction that simultaneously performs weight smoothing and
        estimates the population model parameters in a fully Bayesian construction. We formulate conditions on known marginal and 
        pairwise inclusion probabilities that define a class of sampling designs where $L_{1}$ consistency of the joint posterior is guaranteed. 
        We compare performances between the two approaches on synthetic data, which reveals that our fully Bayesian approach better estimates posterior 
        uncertainty without a requirement to calibrate the normalization of the sampling weights. We demonstrate our method on an application concerning 
        the National Health and Nutrition Examination Survey exploring the relationship between caffeine consumption and systolic blood pressure.'''

    llms = [
        ChatOpenAI(model="gpt-3.5-turbo-0613", temperature=0.9),
        Replicate(
            model="meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
            model_kwargs={"temperature": 0.9, "max_length": 500, "top_p": 1},
        )
    ]
    llm_mediator = ChatOpenAI(model="gpt-3.5-turbo-0613", temperature=0.9)

    handler = LLMChainHandler(llm_mediator=llm_mediator,
                              llms=llms,
                              labels=labels,
                              description=description)
    final_labels, explanation = handler.run()
    print(final_labels)
    print(explanation)
