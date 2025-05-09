

from agents import Agent, InputGuardrail,GuardrailFunctionOutput, Runner, ItemHelpers, TResponseInputItem, trace
from pydantic import BaseModel
import asyncio
from dtos import CodeTask, CodeSolution, CodeFeedback
import logging 
import logging_config

logger = logging.getLogger(__name__)

python_coder_agent = Agent(
    model="o3-mini",
    name="Coder",
    handoff_description="Specialist agent for writing python code and test cases",
    instructions="You are a expert software engineer coding in python, who follows best practices and writes testable code. Write code based on task description by user.",
    output_type=CodeSolution,
)
reviewer_agent = Agent(
    model="o3-mini",
    name="Reviewer",
    handoff_description="Specialist agent for reviewing python code, ensures that code is well written and follows best practices",
    instructions="You are a expert code reviewer that reviews code in python. Validate that code is fully implemented, it follows user requirement, and provides feedback for correction and improvement.",
    output_type=CodeFeedback,
)

async def generate_solution(task_content: str) -> CodeSolution:
    """Generate code solution based on task description."""

    max_iterations = 3
    iteration = 1
    coder_convo_history = []
    reviewer_convo_history = []

    coder_convo_history.append({"role": "user", 
                                "content": task_content })
    reviewer_convo_history.append({"role": "user",
                                   "content": f"Task description : \n{task_content}",
                             })
    logger.info("Generating code ...")
    code_solution = await Runner.run(python_coder_agent, coder_convo_history)
    #.final_output_as(CodeSolution)
    logger.info("Generated code.")
    for i in range(1, max_iterations+1):
        logger.info(f"Iteration {i} of feedback..")
        iteration = i
        reviewer_convo_history.append({"role": "user",
                                       "content": f"Please provide feedback on code solution {i} : \n{code_solution.final_output.code} ",
                                 })
        code_feedback = await Runner.run(reviewer_agent, reviewer_convo_history)
        #.final_output_as(CodeFeedback)
        logger.info("Received feedback")
        if code_feedback.final_output.refine_further:
            logger.info("Need further refinement.")
            coder_convo_history.append({"role": "user",
                                        "content": f"Please improve the code based on feedback : \n{code_feedback.final_output.feedback} "})
            logger.info("Refining code ...")
            code_solution = await Runner.run(python_coder_agent, coder_convo_history)
            #.final_output_as(CodeSolution)
            logger.info("Refined code.")
        else:
            logger.info("Don't need further refinement.")
            break
    return code_solution, iteration
