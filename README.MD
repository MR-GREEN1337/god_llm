![God](assets/god_llm.png)
<a href="https://www.freepik.com/search">Icon by mangsaabguru</a>

### TODO: Include tools such as tavily and RAG.

### 20/10/2024
problems faced: graphs diverges from the prompt's initial idea, starts babbling on different stuff.

## expand() seems to run infinitely, so i should fix that
## Implement tests
## Implement function calling in BaseLLM inheritor classes, in on method take prompt, use function calling to see if LLM needs call function, of so do so inside method and generate finally, BE ABLE TO use it as llm.with_tools(tools), tools:List[BaseTool], have off-the-shelf tools, and be able to create custom tools.
## Implement better visualisation method

# Done
## Add method of detailing report
## while expanding, if node is irrelevant, just delete it. 
## The more you get deeper, the more the llm forgets about initial prompt, so on in every thought generation, be able to retrieve previous parents contexts
## Implement better prompt templates that ground the llm to go straight into the point, no babbling arounds
## Implement DEBUG=True | False, To conditionally log done