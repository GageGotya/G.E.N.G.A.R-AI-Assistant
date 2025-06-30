#!/usr/bin/env python3
"""
AI Handler for G.E.N.G.A.R
Author: Gage Ayala
"""

import asyncio
import logging
from typing import Optional

class AIHandler:
    """Handles AI interactions and responses"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger("GENGAR.AI")
        self.api_key = config.get("openai_api_key", "")
        
        # Initialize AI model
        self.model = config.get("ai_model", "gpt-4")
        
        # Cybersecurity context for better responses
        self.context = """
        You are G.E.N.G.A.R (Gage's Enhanced Next-Gen AI Responder), an AI assistant 
        specialized in cybersecurity, penetration testing, and offensive security. 
        
        You help with:
        - Explaining security concepts and vulnerabilities
        - Providing guidance on penetration testing methodologies
        - Assisting with CTF challenges and techniques
        - Explaining tools and their usage
        - Offering security best practices
        
        Always provide accurate, educational, and ethical guidance. Focus on 
        defensive security and authorized testing only.
        """
    
    async def process(self, user_input: str) -> str:
        """Process user input and return AI response"""
        try:
            # Check if OpenAI API is configured
            if not self.api_key:
                return self.get_fallback_response(user_input)
            
            # Process with OpenAI (placeholder for now)
            response = await self._call_openai(user_input)
            return response
            
        except Exception as e:
            self.logger.error(f"Error processing AI request: {e}")
            return self.get_fallback_response(user_input)
    
    async def _call_openai(self, user_input: str) -> str:
        """Call OpenAI API (placeholder implementation)"""
        # This would be implemented with actual OpenAI API calls
        # For now, return a fallback response
        return self.get_fallback_response(user_input)
    
    def get_fallback_response(self, user_input: str) -> str:
        """Get fallback response when AI is not available"""
        user_input_lower = user_input.lower()
        
        # Cybersecurity-related responses
        if any(word in user_input_lower for word in ['sql injection', 'sqli']):
            return """
🔍 SQL Injection (SQLi) is a web security vulnerability that allows attackers to 
interfere with database queries. It occurs when user input is directly concatenated 
into SQL statements without proper sanitization.

Common types:
• Union-based SQLi
• Boolean-based SQLi  
• Time-based SQLi
• Error-based SQLi

Prevention: Use parameterized queries, input validation, and proper escaping.
            """
        
        elif any(word in user_input_lower for word in ['privilege escalation', 'privesc']):
            return """
🔐 Privilege Escalation is the process of gaining higher-level permissions on a 
system than originally intended. This is a critical phase in penetration testing.

Common techniques:
• Linux: SUID binaries, cron jobs, kernel exploits
• Windows: Token manipulation, service abuse, registry exploits
• Web: File upload bypass, command injection

Tools: LinPEAS, WinPEAS, PowerSploit, Metasploit
            """
        
        elif any(word in user_input_lower for word in ['nmap', 'scan']):
            return """
📡 Nmap is a powerful network scanning tool used for discovery and security auditing.

Common commands:
• nmap -sC -sV [IP] - Basic scan with scripts and version detection
• nmap -p- [IP] - Scan all ports
• nmap --script vuln [IP] - Vulnerability scan
• nmap -A [IP] - Aggressive scan

Remember to only scan systems you own or have permission to test.
            """
        
        elif any(word in user_input_lower for word in ['ctf', 'capture the flag']):
            return """
🏁 Capture The Flag (CTF) competitions are cybersecurity challenges that test 
various skills including:

Categories:
• Web Exploitation - SQLi, XSS, file uploads
• Reverse Engineering - Binary analysis, malware analysis
• Cryptography - Encryption/decryption challenges
• Forensics - File analysis, memory dumps
• Steganography - Hidden data in files/images

Platforms: TryHackMe, Hack The Box, PicoCTF, OverTheWire
            """
        
        elif any(word in user_input_lower for word in ['metasploit', 'msf']):
            return """
💥 Metasploit Framework is a penetration testing platform that provides tools for:

• Exploit development and execution
• Post-exploitation modules
• Payload generation
• Auxiliary modules for reconnaissance

Common commands:
• msfconsole - Start Metasploit console
• search [exploit] - Search for exploits
• use [module] - Load a module
• set [option] [value] - Configure options
• exploit - Execute the module

Always use responsibly and only on authorized systems.
            """
        
        elif any(word in user_input_lower for word in ['help', 'what can you do']):
            return """
🤖 I'm G.E.N.G.A.R, your cybersecurity AI assistant! I can help with:

🔍 Security Concepts:
• Explaining vulnerabilities and attack vectors
• Describing penetration testing methodologies
• Clarifying security tools and their usage

🏁 CTF Assistance:
• Explaining challenge types and techniques
• Providing guidance on problem-solving approaches
• Sharing relevant tools and resources

🛠️ Technical Support:
• Command explanations and usage
• Tool recommendations for specific tasks
• Best practices and security guidelines

💡 Just ask me about any cybersecurity topic, tool, or technique!
            """
        
        else:
            return f"""
🤖 I understand you're asking about: "{user_input}"

I'm G.E.N.G.A.R, a cybersecurity-focused AI assistant. I can help with:
• Security concepts and vulnerabilities
• Penetration testing techniques
• CTF challenges and problem-solving
• Tool usage and recommendations
• Security best practices

Try asking me about specific topics like "SQL injection", "privilege escalation", 
"nmap scanning", or "CTF challenges" for detailed explanations!
            """
    
    def is_cybersecurity_related(self, user_input: str) -> bool:
        """Check if user input is cybersecurity-related"""
        security_keywords = [
            'hack', 'security', 'vulnerability', 'exploit', 'penetration',
            'ctf', 'flag', 'shell', 'reverse', 'payload', 'injection',
            'xss', 'sqli', 'csrf', 'lfi', 'rfi', 'privesc', 'escalation',
            'nmap', 'metasploit', 'burp', 'wireshark', 'kali', 'linux',
            'windows', 'network', 'port', 'scan', 'firewall', 'vpn',
            'encryption', 'crypto', 'hash', 'password', 'brute', 'force'
        ]
        
        user_input_lower = user_input.lower()
        return any(keyword in user_input_lower for keyword in security_keywords) 