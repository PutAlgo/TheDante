import asyncio
import os
from aiohttp import ClientSession, TCPConnector
import ssl
import openai
from langchain import OpenAI
from llama_index import SimpleDirectoryReader, ServiceContext, VectorStoreIndex, set_global_service_context
from llama_index.response.pprint_utils import pprint_response
from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index.query_engine import SubQuestionQueryEngine
from langchain import PromptTemplate as PromptTemp
from langchain.chat_models import ChatOpenAI
# Async function to handle each query
async def handle_query(catalent_engine, category, query, prompt):
    print(f"\nProcessing query: {query}")
    response = await catalent_engine.aquery(prompt.format(query=query, llm=ChatOpenAI(model_name="gpt-3.5-turbo")))
    return category, query, response

def gpt_doc(name,meta):
    async def main():
        sslcontext = ssl.create_default_context()
        sslcontext.check_hostname = False
        sslcontext.verify_mode = ssl.CERT_NONE
        openai.api_key = os.getenv("OPENAI_API_KEY")

        async with ClientSession(connector=TCPConnector(ssl_context=sslcontext)) as session:
            async with session.get('https://api.openai.com/v1/engines/text-davinci-003/completions') as resp:
                print(resp.status)

        llm = OpenAI(temperature=0, model_name="gpt-3.5-turbo", max_tokens=-1)
        service_context = ServiceContext.from_defaults(llm=llm)
        set_global_service_context(service_context=service_context)

        template = '''Please use this template to conduct an unbiased analysis of a company's 10-K SEC filings, 
                    with the aim of identifying potential fraudulent activity. Ensure your analysis is data-driven and 
                    centered on numerical discrepancies, unexpected changes, and potentially suspicious activities.

                    Your analysis should consider:
                    
                    Item 8 - Financial Statements and Supplementary Data: This section holds crucial information about a company's financial status. Keep an eye out for abrupt, unaccounted changes in key metrics such as operating margins, return on equity, cash conversion cycle, or inventory turnover. Such changes could signify possible fraudulent activity.
                    
                    Footnotes: These reveal essential information about a company's accounting practices, estimates, and assumptions. Any abrupt changes in these areas can serve as a red flag.
                    
                    Item 9A - Controls and Procedures: This section discusses the company's internal controls over financial reporting. Disclosures of significant deficiencies or material weaknesses in internal controls can be indicative of potential fraud.
                    
                    Item 6 - Selected Financial Data: This section offers a five-year comparative overview of key financial data. Be alert to abrupt changes or inconsistencies in trends, which could be potential fraud indicators.
                    
                    Auditor's Report: This section holds the independent auditor's opinion on the financial statements' fairness. Anything other than an "unqualified" opinion could raise red flags.
                    
                    Exhibits: This section contains all significant contracts, agreements, and documents. Scrutinize these for unusual transactions, especially those involving related parties.
                    
                    Earnings Restatements: If a company frequently needs to restate its earnings, it might suggest issues with its financial reporting practices.
                    
                    Cash Flow Analysis: This statement shows the cash generated or used by a company during a given period. If a company reports high revenues but decreasing cash from operations, it might be inflating its revenue.
                    
                    
                    The following examples illustrate both fraudulent and legitimate cases across different items. Use these as a guide to distinguish between genuine and fraudulent reporting.
                                                                             
                    Item 6 - Selected Financial Data
                    
                    Fraudulent: TechBoost reports a $100 million revenue spike. However, investigation reveals a premature $50 million recognition from a 2024 software licensing deal, inflating 2023 revenue by 25%.
                    Legitimate: TechBoost's revenue genuinely increases by $100 million due to a successful product launch. The MD&A provides a clear breakdown of the new revenue streams.
                    Item 7 - Management's Discussion and Analysis of Financial Condition and Results of Operations (MD&A)
                    
                    Fraudulent: TechBoost shows a net income drop, attributing it to "one-off restructuring costs". However, specifics about these costs are not provided, potentially hiding ongoing profitability issues.
                    Legitimate: TechBoost's net income decreases due to unexpected tariff changes. The MD&A explains this and outlines measures for mitigation, like alternative sourcing.
                    Item 8 - Financial Statements and Supplementary Data
                    
                    Fraudulent: TechBoost's balance sheet includes an unexplained $250 million "miscellaneous assets" entry. Investigation reveals overvalued goodwill from an acquisition, artificially inflating total assets.
                    Legitimate: TechBoost's assets increase due to an acquisition. This is clearly disclosed in the financial statements notes.
                    Item 9A - Controls and Procedures
                    
                    Fraudulent: TechBoost has a revenue recognition process loophole leading to a prior year's $20 million overstatement. This control weakness isn't reported or rectified.
                    Legitimate: TechBoost identifies an inventory control weakness, leading to a $5 million write-down. The 10-K outlines this issue and remediation measures, like a new inventory tracking system.
                    Auditor's Report
                    
                    Fraudulent: TechBoost frequently changes auditors, and the current report contains a qualification about revenue recognition inconsistency without clarification.
                    Legitimate: The auditor's report, from a Big Four accounting firm, states TechBoost's financial statements present the company's financial position fairly.
                    Exhibits
                    
                    Fraudulent: TechBoost discloses a complex transaction with a related off-balance-sheet entity, BrightFin. The transaction isn't clearly explained, potentially hiding liabilities.
                    Legitimate: TechBoost discloses a new patent agreement. The agreement is detailed, and its impact on financial statements and business prospects is explained.
                    
                                        
                    After completing your analysis, start your response with one of the following signals based on your findings:

                    "Red Flag" - If there are clear signs of potential fraudulent activity, pointing out the data points that led you to this conclusion, including any drastic changes or inconsistencies in financial values over the years.
                    
                    "Yellow Flag" - If there are areas that raise suspicions or need further investigation, highlighting the specific financial indicators that raised your concerns and why you believe they deserve further investigation.
                    
                    "Green Flag" - If your analysis does not uncover any suspicious or fraudulent activities in the financial statements. Explain the data points that affirm the company's clean financial health.
                    
                    Now, please conduct the analysis:
                    
                    Question:{query}'''



        prompt = PromptTemp(template=template, input_variables=["query"])

        catalent_docs = SimpleDirectoryReader(input_files=[f"/Users/matthewarciuolo/Interface-2/{name}"]).load_data()

        print(f'Loaded {name} with {len(catalent_docs)} pages')

        catalent_index = VectorStoreIndex.from_documents(catalent_docs)

        catalent_engine = catalent_index.as_query_engine(similarity_top_k=3)

        year1 = f"20{meta['range'][0]}"
        year2 = f"20{meta['range'][1]}"
        entity_name = name
        print('what')
        # We assign a weight to each query based on its importance in the context of fraud detection
        query_weights = {

            "Improper Timing of Revenue Recognition": [
                f"Identify any instances of significant quarter-end sales or revenue 'pull-ins' from future quarters for {entity_name} between {year1} and {year2}.",
                f"Find instances where {entity_name}'s income smoothing caused a substantial change in net income from {year1} to {year2}."
            ],
            "Fictitious Revenue": [
                f"Detect any sudden or unexplained increase in {entity_name}'s revenue or sales to potentially fictitious customers from {year1} to {year2}.",
                f"Track any inconsistencies or anomalies in {entity_name}'s sales or revenue patterns from {year1} to {year2}."
            ],
            "Channel Stuffing": [
                f"Locate any instances of substantial quarter-end sales or abnormally high inventory levels at distributors for {entity_name} between {year1} and {year2}.",
                f"Detect any rapid increase in {entity_name}'s revenues without corresponding increases in accounts receivable and inventory from {year1} to {year2}."
            ],
            "Third-Party Transactions": [
                f"Track any bill and hold sales, consignment sales, side letter agreements, and other contingent sales by {entity_name} from {year1} to {year2}.",
                f"Identify instances where {entity_name} recognized revenue from products stored at a third-party's warehouse between {year1} and {year2}."
            ],
            "Fraudulent Management Estimates": [
                f"Find any instances where {entity_name}'s methodology to determine write-offs or adjustments was changed or appears inconsistent from {year1} to {year2}.",
                f"Detect any sudden changes in {entity_name}'s earnings forecasts or other financial estimates between {year1} and {year2}."
            ],
            "Improper Capitalization of Expenses": [
                f"Identify any significant increase in capitalized expenses that do not appear to benefit future periods for {entity_name} between {year1} and {year2}.",
                f"Track any inconsistencies or unexplained patterns in {entity_name}'s capitalization of expenses from {year1} to {year2}."
            ],
            "Other Improper Expense Recognition Schemes": [
                f"Detect any instances of inappropriate deferring of current period expenses, improper allocation of costs to inventory, or unusual patterns in reserves for {entity_name} between {year1} and {year2}.",
                f"Find any instances where {entity_name} might have understated reserves for bad debt and loan losses, or failed to record asset impairments from {year1} to {year2}."
            ],
            "Misleading Forecasts or Projections": [
                f"Identify any instances where {entity_name} may have issued misleading forecasts or avoided disclosing an increased risk of missing key financial goals between {year1} and {year2}.",
                f"Detect any significant discrepancies between {entity_name}'s public and internal forecasts or projections from {year1} to {year2}."
            ],
            "Misleading Non-GAAP Reporting": [
                f"Identify instances where {entity_name} may have manipulated non-GAAP metrics to reflect stronger growth or higher earnings from {year1} to {year2}.",
                f"Track any inconsistencies between {entity_name}'s GAAP and non-GAAP figures from {year1} to {year2}."
            ],
            "Inadequate Internal Controls over Financial Reporting": [
                f"Determine any instances of failure to account for substantial amounts of revenue, or instances where {entity_name} failed to recognize all of the related program costs between {year1} and {year2}.",
                f"Find any evidence of weak or inadequate internal controls over financial reporting at {entity_name} from {year1} to {year2}."
            ]
    }

        array_flags = {'red': [], 'green': [], 'yellow': []}
        tasks = []

        if meta['focus'] == 'selectAll':
            for category, val in query_weights.items():
                print(category)
                for query in val:
                    tasks.append(handle_query(catalent_engine, category, query, prompt))

        else:
            for query in query_weights[meta['focus']]:
                tasks.append(handle_query(catalent_engine,  meta['focus'], query, prompt))

        responses = await asyncio.gather(*tasks)

        for category, query, response in responses:
            print(f"{category}, {query}, {response}")
            if response.response.__contains__("Green flag:"):
                print(f"Green Flag: {response}")
                array_flags['green'].append((category, response))

            elif response.response.__contains__("Red Flag:"):
                print(f"Red Flag: {response}")
                array_flags['red'].append((category, response))

            elif response.response.__contains__("Yellow Flag:"):
                print(f"Yellow Flag: {response}")
                array_flags['yellow'].append((category, response))

            else:
                print("error")

        return array_flags

    return asyncio.run(main())

    # Run the main function



