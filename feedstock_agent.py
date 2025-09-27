from openai import OpenAI
import json
import typing

client = OpenAI()
model = "gpt-4.1"

def get_response(instructions: str, input: str):
    try:
        response = client.responses.create(
            model=model,
            instructions=instructions, #system prompt
            input=input # user prompt
        )
        return response.output_text
    except:
        with Exception as e:
            print(f"""Call to LLM failed: {e}""")


def feedstock_analyst_agent(feedstock_name):
    # Analyze the hydrocarbon feed
    '''
    Args:
        feedstock_name(str), e.g., "Light Sweet Crude"
        
    Returns:
        String of an analysis of the given feedstock

    '''
    
    instructions = f"""
    You are a petrochemical expert analyzing hydrocarbon feedstocks. 
    """
    
    input = f"""
    Analyze the feedstock: {feedstock_name}
    
    Provide a concise analysis of the given feedstock, highlighting its key 
    components and general suitability for producing valuable refined products 
    like gasoline, diesel, and kerosene.
    """
    
    print(f"""Analyzing {feedstock_name}, please be patient.""")
    response = get_response(instructions, input)
    print("Analysis done!")
    print("-------------------------")
    print()
    return response

def distillation_planner_agent(feedstock_analysis):
    # Allocate through distillation tower
    '''
    args:
        feedstock_analysis (str): response from feedstock_analyst_agent
        
    returns:
        Dictionary of potential percentage yields for products
    '''
    
    instructions = f'''
    You are a refinery distillation tower operations planner. 
    
    '''
    
    input = f'''
    Based on the provided feedstock analysis below, estimate the potential percentage yields for major products like gasoline, diesel, and kerosene. Be realistic.
    
    Provide your output as a JSON. Return only the JSON.
    
    Example output:
    ```json
    {{
        "gasoline": "40%",
        "diesel": "30%",
        "kerosene": "20%",
        "other": "10%"
    }}
    ```
    
    FEEDSTOCK ANALYSIS:
    {feedstock_analysis}
    '''
    
    print("Estimating percentage yields")
    response = get_response(instructions, input)
    print("-------------------")
    
    # Parse the response
    json_text = response.strip()

    if "```json" in json_text:
        json_text = json_text.split("```json")[1].split("```")[0].strip()
    print(json_text)
    return json.loads(json_text)

def market_analyst_agent(product_list):
    # Analyze market conditions
    '''
    args:
        product_list (dict): Dictionary of potential percentage yields for products
        
    returns:
        A string with market analysis, demand levels, and profitability.

    '''
    instructions = "You are an energy market analyst."
    
    products = ",".join([key for key in product_list.keys()])
    
    input = f"""For the following list of refined products, 
    provide a brief analysis of current market demand (high, medium, low) 
    and general profitability trends.
    
    LIST OF REFINED PRODUCTS: {products}"""
    
    print("Analyzing products")
    response = get_response(instructions, input)
    print("-------------------")
    print()
    return response

def production_optimizer_agent(distillation_plan, market_data):
    '''
    args:
        distillation_plan (output from distillation_planner_agent), 
        market_data: output from market_analyst_agent
        
    returns:
        a string recommendation on production focus
    '''
    instructions = f"""You are a refinery production optimization expert. 
    Your goal is to recommend a production strategy based on potential yields and current market conditions."""
    
    input = f"""
    Given the following potential distillation plan:
    --- DISTILLATION PLAN ---
    {distillation_plan}
    --- END DISTILLATION PLAN ---
    And the following market analysis:
    --- MARKET ANALYSIS ---
    {market_data}
    --- END MARKET ANALYSIS ---
    Please provide a concise recommendation on which products the refinery should prioritize or focus on to maximize value, 
    considering both the potential yield and market conditions.
    """

    print("Creating recommendations for products")
    response = get_response(instructions, input)
    print("-------------------")
    print()
    return response

def main(feedstock_name):
    feedstock_analysis = feedstock_analyst_agent(feedstock_name)
    print(f"""Analysis of {feedstock_name}""")
    print(feedstock_analysis)
    print("-------------------------")
    print()
    
    product_yields = distillation_planner_agent(feedstock_analysis)
    market_analysis = market_analyst_agent(product_yields)
    
    distillation_plan = "Based on the analysis, potential yields are: "
    for key, value in product_yields.items():
        distillation_plan += f"""{key}: {value} """
        
    result = production_optimizer_agent(distillation_plan, market_analysis)
    print("RECOMMENDATION:")
    print(result)


if __name__ == "__main__":
    main("Light Sweet Crude")