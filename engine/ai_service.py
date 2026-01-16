import google.generativeai as genai
import os
import json
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self, api_key: str):
        if not api_key:
            logger.warning("GEMINI_API_KEY not provided. AI features will be disabled.")
            self.model = None
        else:
            try:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-1.5-pro')
                logger.info("AI Service initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize AI service: {str(e)}")
                self.model = None

    async def analyze_report(self, contract_address: str, slither_output: dict) -> str:
        """
        Analyze Slither results using Gemini AI and provide contextual explanations.
        """
        if not self.model:
            return "AI analysis unavailable: GEMINI_API_KEY not configured."

        try:
            system_prompt = """You are a Senior Smart Contract Auditor and Security Researcher (MamoruAI).
Your task is to analyze the following static analysis report (from Slither) and provide a professional, 
contextual explanation of the vulnerabilities found.

For each vulnerability:
1. Explain the technical cause in clear terms.
2. Assess the real-world impact and potential exploit scenarios.
3. Provide clear, actionable remediation steps with code examples if applicable.

Format your response in structured Markdown with clear sections.
Be concise but thorough. If no critical vulnerabilities are found, acknowledge the security posture.
Focus on practical, actionable advice for developers."""

            # Extract key information for the prompt
            vulnerabilities = slither_output.get('vulnerabilities', [])
            statistics = slither_output.get('statistics', {})
            
            prompt = f"""Contract Address: {contract_address}

Security Analysis Summary:
- Total Vulnerabilities: {statistics.get('total_vulnerabilities', 0)}
- Critical: {statistics.get('critical', 0)}
- High: {statistics.get('high', 0)}
- Medium: {statistics.get('medium', 0)}
- Low: {statistics.get('low', 0)}

Detailed Vulnerabilities:
{json.dumps(vulnerabilities[:10], indent=2)}  # Limit to first 10 for token efficiency

Please provide a comprehensive security report analyzing these findings. Include:
1. Executive summary of the security posture
2. Detailed analysis of each critical/high severity vulnerability
3. Recommended remediation steps
4. Overall risk assessment

Format the response in clear Markdown with proper headings."""

            logger.info("Sending analysis request to Gemini AI")
            response = self.model.generate_content([system_prompt, prompt])
            
            if response and response.text:
                logger.info("AI analysis completed successfully")
                return response.text
            else:
                logger.warning("AI returned empty response")
                return "AI analysis completed but returned no content."

        except Exception as e:
            logger.error(f"Error in AI analysis: {str(e)}")
            return f"AI analysis failed: {str(e)}. Please review Slither results directly."
