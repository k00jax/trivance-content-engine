"""
Content Vault - Store and manage successful AI-generated content examples
"""
import json
import os
from datetime import datetime
from typing import Dict, Any, List

class ContentVault:
    def __init__(self, vault_path: str = "data/content_vault.json"):
        self.vault_path = vault_path
        self.ensure_vault_exists()
    
    def ensure_vault_exists(self):
        """Create the vault file if it doesn't exist"""
        os.makedirs(os.path.dirname(self.vault_path), exist_ok=True)
        if not os.path.exists(self.vault_path):
            self._save_vault({"successful_posts": [], "stats": {"total_stored": 0}})
    
    def _load_vault(self) -> Dict[str, Any]:
        """Load the content vault from file"""
        try:
            with open(self.vault_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {"successful_posts": [], "stats": {"total_stored": 0}}
    
    def _save_vault(self, vault_data: Dict[str, Any]):
        """Save the content vault to file"""
        with open(self.vault_path, 'w', encoding='utf-8') as f:
            json.dump(vault_data, f, indent=2, ensure_ascii=False)
    
    def store_successful_post(self, article_title: str, generated_post: str, metadata: Dict[str, Any]):
        """Store a successful post with metadata"""
        vault_data = self._load_vault()
        
        post_entry = {
            "timestamp": datetime.now().isoformat(),
            "article_title": article_title,
            "generated_post": generated_post,
            "character_count": len(generated_post),
            "method": metadata.get("method", "unknown"),
            "style_used": metadata.get("style_used", "unknown"),
            "platform": metadata.get("platform", "unknown"),
            "token_usage": metadata.get("token_usage", {}),
            "generation_time": metadata.get("generation_time", 0)
        }
        
        vault_data["successful_posts"].append(post_entry)
        vault_data["stats"]["total_stored"] = len(vault_data["successful_posts"])
        
        self._save_vault(vault_data)
        print(f"💾 Stored successful post in content vault ({len(vault_data['successful_posts'])} total)")
    
    def get_recent_successes(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get recent successful posts"""
        vault_data = self._load_vault()
        return vault_data["successful_posts"][-limit:]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get vault statistics"""
        vault_data = self._load_vault()
        posts = vault_data["successful_posts"]
        
        if not posts:
            return {"total_posts": 0}
        
        methods = {}
        styles = {}
        avg_length = 0
        
        for post in posts:
            method = post.get("method", "unknown")
            style = post.get("style_used", "unknown")
            
            methods[method] = methods.get(method, 0) + 1
            styles[style] = styles.get(style, 0) + 1
            avg_length += post.get("character_count", 0)
        
        return {
            "total_posts": len(posts),
            "average_length": avg_length // len(posts) if posts else 0,
            "methods_used": methods,
            "styles_used": styles,
            "latest_post": posts[-1]["timestamp"] if posts else None
        }

# Global vault instance
content_vault = ContentVault()
