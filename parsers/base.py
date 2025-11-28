from abc import ABC, abstractmethod
from typing import List, Dict
from pathlib import Path

"""
Base Parser - Abstract class for all dependency parsers.

Java equivalent:
public abstract class BaseParser {
    public abstract List<Dependency> parse(String filepath);
}
"""

class BaseParser(ABC):
     """
    Abstract base class for dependency parsers.
    
    In Java, you'd use either an interface or abstract class:
    public interface Parser {
        List<Dependency> parse(String filepath) throws IOException;
    }
    
    In Python, we use ABC (Abstract Base Class) from the abc module.
    """
    @abstractmethod
    def parse(self, filepath) 
    """
        Parse dependencies from a file.
        
        Args:
            filepath (str): Path to dependency file
            
        Returns:
            list: List of dependency dictionaries with keys:
                  - name: package name
                  - version: package version
                  - ecosystem: package ecosystem (pip, maven, etc.)
        
        Java equivalent:
        public abstract List<Dependency> parse(String filepath) 
            throws IOException;
        """
        pass

    def read_file(self, filepath):
        """
        Helper method to read file contents.
        
        Java equivalent:
        protected String readFile(String filepath) throws IOException {
            return Files.readString(Path.of(filepath));
        }
        """
        # Path is like Java NIO's Path
        path = Path(filepath)
        
        # Check if file exists
        if not path.exists():
            # Raise exception (like throw new FileNotFoundException())
            raise FileNotFoundError(f"File not found: {filepath}")
        
        # Read entire file as string
        # Java: return Files.readString(path);
        return path.read_text()