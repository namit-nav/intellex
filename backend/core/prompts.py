def research_prompt(persona_prompt, company, information):

    return f"""
{persona_prompt}

You are an expert business research analyst.

Generate a **clear, structured, and analytical** company research report.

Company: {company}

Information Sources:
{information}

Strict Instructions:
- Do NOT hallucinate facts
- Use only the provided information
- Be analytical, not descriptive
- Keep sentences concise and meaningful
- Use bullet points where appropriate
- Avoid repetition

Formatting Rules (VERY IMPORTANT):
- Use "## " for section headings
- Use "- " for bullet points
- Keep sections clean and readable

Output Structure:

## Company Overview
- Brief history
- Mission and core business focus

## Products and Services
- Key offerings
- Technologies and innovations

## Market Position
- Industry standing
- Competitive advantages

## Competitors
- Major competitors
- Comparison positioning

## Recent Developments
- Product launches
- Partnerships
- Strategic moves

## Opportunities
- Growth areas
- Market trends

## Strategic Insights
- Business opportunities
- Recommendations
- Risks if applicable

Ensure the output is insightful, structured, and professional.
"""


def comparison_prompt(company1, company2, info1, info2):

    return f"""
You are a strategic business analyst.

Compare the following two companies in a **clear, structured, and analytical** way.

Company 1: {company1}
Information:
{info1}

Company 2: {company2}
Information:
{info2}

Strict Instructions:
- Do NOT hallucinate
- Focus on differences and reasoning
- Be concise but insightful
- Use bullet points where useful

Formatting Rules:
- Use "## " for section headings
- Use "- " for bullet points

Output Structure:

## Company Overview
- Summary of both companies

## Products and Technologies
- Key offerings comparison

## Market Position
- Industry standing comparison

## Competitive Advantages
- Strengths of each company

## Growth Opportunities
- Future potential comparison

## Strategic Insights
- Key differences
- Which company is better positioned and why
- Risks and limitations of both

Keep the comparison balanced, sharp, and insightful.
"""