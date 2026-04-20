def research_prompt(persona_prompt, company, information):

    return f"""
{persona_prompt}

You are an expert business research analyst.

Generate a detailed and professional company research report.

Company: {company}

Information Sources:
{information}

Instructions:
- Be analytical, not just descriptive
- Use bullet points where possible
- Avoid vague statements
- Focus on insights and reasoning

Structure your response clearly:

1. Company Overview
- Brief history
- Mission and core business focus

2. Products and Services
- Key offerings
- Important technologies or innovations

3. Market Position
- Industry standing
- Competitive advantages

4. Competitors
- Major competitors
- How this company compares

5. Recent Developments
- Product launches
- Partnerships
- Strategic moves

6. Opportunities
- Growth areas
- Market trends benefiting the company

7. Strategic Account Plan
- Business opportunities
- Potential partnerships
- Strategic recommendations

Make the output structured, clear, and insightful.
"""

def comparison_prompt(company1, company2, info1, info2):

    return f"""
You are a strategic business analyst.

Compare the following two companies in a clear and analytical way.

Company 1: {company1}
Information:
{info1}

Company 2: {company2}
Information:
{info2}

Instructions:
- Highlight key differences clearly
- Explain WHY the companies differ
- Compare business models and strategies
- Provide deeper insights, not just descriptions
- Use bullet points where possible

Structure:

1. Company Overview
2. Key Products and Technologies
3. Market Position
4. Competitive Advantages
5. Growth Opportunities
6. Strategic Insights
- Key differences between the companies
- Which company is better positioned for future growth and why
- Risks and limitations of each company

Make the comparison concise, structured, and insightful.
"""