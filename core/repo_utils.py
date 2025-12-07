"""
Utility functions for repository operations
"""
import os
import shutil
import tempfile
from pathlib import Path
from typing import List, Tuple
import git


# Supported file extensions by language
LANGUAGE_EXTENSIONS = {
    'python': ['.py'],
    'javascript': ['.js', '.jsx', '.ts', '.tsx'],
    'java': ['.java'],
    'cpp': ['.cpp', '.cc', '.cxx', '.h', '.hpp'],
    'go': ['.go'],
    'rust': ['.rs']
}

# Directories to skip during file discovery
SKIP_DIRECTORIES = {
    '.git', '.github', 'node_modules', '__pycache__', 
    'venv', '.venv', 'env', '.env',
    'dist', 'build', 'out', 'target',
    '.next', '.nuxt', 'coverage',
    'vendor', 'packages'
}

# Files to skip
SKIP_FILES = {
    '__init__.py',  # Often empty
    'setup.py',     # Config file
    'conftest.py'   # Test config
}


def clone_repository(github_url: str, temp_dir: str = None) -> Tuple[str, dict]:
    """
    Clone a GitHub repository to a temporary directory.
    
    Args:
        github_url: GitHub repository URL
        temp_dir: Optional temp directory path
        
    Returns:
        Tuple of (repo_path, metadata)
    """
    try:
        # Create temp directory if not provided
        if temp_dir is None:
            temp_dir = tempfile.mkdtemp(prefix='code_inspector_')
        
        print(f"🔄 Cloning repository to {temp_dir}...")
        
        # Clone the repository (shallow clone for speed)
        repo = git.Repo.clone_from(github_url, temp_dir, depth=1)
        
        # Extract metadata
        repo_name = github_url.rstrip('/').split('/')[-1].replace('.git', '')
        
        metadata = {
            'repo_name': repo_name,
            'url': github_url,
            'clone_path': temp_dir,
            'branch': repo.active_branch.name if hasattr(repo, 'active_branch') else 'main'
        }
        
        print(f"✅ Successfully cloned {repo_name}")
        return temp_dir, metadata
        
    except Exception as e:
        print(f"❌ Error cloning repository: {e}")
        raise


def discover_code_files(repo_path: str, 
                       languages: List[str] = None,
                       max_files: int = 50) -> List[dict]:
    """
    Discover all code files in the repository.
    
    Args:
        repo_path: Path to cloned repository
        languages: List of languages to include (None = all)
        max_files: Maximum number of files to analyze
        
    Returns:
        List of file info dicts with path, language, size
    """
    if languages is None:
        languages = list(LANGUAGE_EXTENSIONS.keys())
    
    # Get all extensions to look for
    extensions = []
    for lang in languages:
        extensions.extend(LANGUAGE_EXTENSIONS.get(lang, []))
    
    code_files = []
    
    # Walk through directory tree
    for root, dirs, files in os.walk(repo_path):
        # Filter out skip directories IN PLACE (modifies dirs)
        dirs[:] = [d for d in dirs if d not in SKIP_DIRECTORIES]
        
        for file in files:
            # Check extension
            if not any(file.endswith(ext) for ext in extensions):
                continue
            
            # Skip certain files
            if file in SKIP_FILES:
                continue
            
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, repo_path)
            
            # Detect language from extension
            language = detect_language_from_path(file_path)
            
            # Get file size
            try:
                size = os.path.getsize(file_path)
                
                # Skip very large files (>100KB)
                if size > 100_000:
                    print(f"⚠️  Skipping large file: {relative_path} ({size} bytes)")
                    continue
                
                code_files.append({
                    'absolute_path': file_path,
                    'relative_path': relative_path,
                    'language': language,
                    'size': size
                })
                
                # Stop if we hit the max
                if len(code_files) >= max_files:
                    print(f"⚠️  Reached max files limit ({max_files})")
                    break
                    
            except Exception as e:
                print(f"⚠️  Error reading {relative_path}: {e}")
                continue
        
        if len(code_files) >= max_files:
            break
    
    print(f"📁 Found {len(code_files)} code files")
    return code_files


def detect_language_from_path(file_path: str) -> str:
    """
    Detect programming language from file extension.
    
    Args:
        file_path: Path to file
        
    Returns:
        Language name (python, javascript, etc.)
    """
    ext = Path(file_path).suffix.lower()
    
    for language, extensions in LANGUAGE_EXTENSIONS.items():
        if ext in extensions:
            return language
    
    return 'unknown'


def read_file_content(file_path: str) -> str:
    """
    Read file content with proper encoding handling.
    
    Args:
        file_path: Path to file
        
    Returns:
        File content as string
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # Try with different encoding
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()
        except Exception as e:
            raise Exception(f"Could not read file: {e}")


def cleanup_repository(repo_path: str):
    """
    Clean up temporary repository directory.
    
    Args:
        repo_path: Path to repository to delete
    """
    try:
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)
            print(f"🗑️  Cleaned up {repo_path}")
    except Exception as e:
        print(f"⚠️  Error cleaning up: {e}")


def get_repository_stats(files: List[dict]) -> dict:
    """
    Calculate basic statistics for repository.
    
    Args:
        files: List of file info dicts
        
    Returns:
        Stats dictionary
    """
    stats = {
        'total_files': len(files),
        'total_size': sum(f['size'] for f in files),
        'languages': {}
    }
    
    # Count by language
    for file in files:
        lang = file['language']
        if lang not in stats['languages']:
            stats['languages'][lang] = 0
        stats['languages'][lang] += 1
    
    return stats
