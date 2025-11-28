import argparse
import sys
from pathlib import Path

# In Python, we import from our own packages like this
# Java equivalent: import com.company.parsers.RequirementsParser;
from parsers.requirements import RequirementsParser
from parsers.pom import PomParser
from api.osv_client import OSVClient
from reporters.report import ReportGenerator

def parse_arguments():
    """
    Parse command-line arguments.
    
    Java equivalent: Using @CommandLineRunner or manually parsing args[]
    
    Python's argparse is much simpler than Apache Commons CLI!
    """
    parser = argparse.ArgumentParser(description='Scan dependencies for vulnerabilities')

    parser.add_argument('--file', required=True, help='Path to the dependency file (e.g., requirements.txt or pom.xml)')

    parser.add_argument(
        '--format',
        choices=['text', 'json', 'html'],
        default='text',
        help='Output format'
    )
    
    parser.add_argument(
        '--output',
        help='Output file path (default: print to console)'
    )
    
    # Parse and return
    # Java: CommandLine cmd = parser.parse(options, args);
    return parser.parse_args()

def detect_file_type(filepath):
    """
    Detect what type of dependency file this is.
    
    Java equivalent:
    private FileType detectFileType(String filepath) {
        if (filepath.endsWith("requirements.txt")) {
            return FileType.REQUIREMENTS;
        }
        // ...
    }
    """
    # Path is like Java's java.nio.file.Path
    path = Path(filepath)
    
    # String comparison (Python strings are objects with methods)
    if path.name == 'requirements.txt':
        return 'requirements'
    elif path.name == 'pom.xml':
        return 'pom'
    else:
        # Raise exception (like throw new IllegalArgumentException())
        raise ValueError(f"Unknown file type: {path.name}")

def get_parser(file_type):
    """
    Factory method to get the right parser.
    
    Java equivalent (Factory pattern):
    public static Parser getParser(FileType type) {
        switch(type) {
            case REQUIREMENTS: return new RequirementsParser();
            case POM: return new PomParser();
            default: throw new IllegalArgumentException();
        }
    }
    """
    # Dictionary as switch statement (Python has no switch until 3.10)
    # Java: Map<String, Supplier<Parser>> parsers = Map.of(...)
    parsers = {
        'requirements': RequirementsParser,
        'pom': PomParser
    }
    
    # Get parser class and instantiate it
    # Java: return parsers.get(file_type).get();
    parser_class = parsers.get(file_type)
    if not parser_class:
        raise ValueError(f"No parser for type: {file_type}")
    
    return parser_class()

def scan_dependencies(filepath):
    """
    Main scanning logic.
    
    This is like a service method in Spring Boot:
    @Service
    public class ScanService {
        public ScanResult scan(String filepath) { ... }
    }
    """
    print(f"📁 Scanning: {filepath}\n")
    
    # Detect file type and get appropriate parser
    file_type = detect_file_type(filepath)
    parser = get_parser(file_type)
    
    # Parse dependencies from file
    # Java: List<Dependency> deps = parser.parse(filepath);
    dependencies = parser.parse(filepath)
    
    if not dependencies:
        print("❌ No dependencies found!")
        return None
    
    print(f"Found {len(dependencies)} dependencies\n")
    
    # Create OSV client (like @Autowired RestTemplate in Spring)
    osv_client = OSVClient()
    
    # Scan each dependency for vulnerabilities
    results = []
    for i, dep in enumerate(dependencies, 1):
        print(f"Checking {i}/{len(dependencies)}: {dep['name']} {dep['version']}")
        
        # Query OSV API
        # Java: VulnResponse response = osvClient.checkVulnerability(dep);
        vulns = osv_client.check_vulnerability(
            package_name=dep['name'],
            version=dep['version'],
            ecosystem=dep['ecosystem']
        )
        
        if vulns:
            results.append({
                'dependency': dep,
                'vulnerabilities': vulns
            })
    
    return results

def display_results(results):
    """
    Display scan results to console.
    
    Java equivalent:
    private void displayResults(List<ScanResult> results) {
        System.out.println("=".repeat(60));
        // ...
    }
    """
    print("\n" + "=" * 62)
    print("VULNERABILITY SCAN SUMMARY")
    print("=" * 62 + "\n")
    
    if not results:
        print("✅ No vulnerabilities found!\n")
        return
    
    # Count totals
    total_packages = len(results)
    total_vulns = sum(len(r['vulnerabilities']) for r in results)
    
    print(f"Total packages scanned: {total_packages}")
    print(f"Vulnerable packages: {total_packages}")
    print(f"Total vulnerabilities: {total_vulns}\n")
    print("⚠️  VULNERABILITIES FOUND:\n")
    
    # Display each vulnerable package
    for result in results:
        dep = result['dependency']
        vulns = result['vulnerabilities']
        
        print(f"  {dep['name']}@{dep['version']}:")
        for vuln in vulns:
            severity = vuln.get('severity', 'UNKNOWN')
            vuln_id = vuln.get('id', 'UNKNOWN')
            print(f"    - {vuln_id} [{severity}]")
        print()
    
    print("=" * 62 + "\n")

def main():
    """
    Main function - program entry point.
    
    Java equivalent: public static void main(String[] args)
    """
    try:
        # Parse command-line arguments
        args = parse_arguments()
        
        # Scan the file
        results = scan_dependencies(args.file)
        
        if results is None:
            sys.exit(1)
        
        # Generate report based on format
        reporter = ReportGenerator()
        
        if args.format == 'text':
            display_results(results)
        elif args.format == 'json':
            output = reporter.generate_json(results)
            if args.output:
                Path(args.output).write_text(output)
                print(f"📄 Report saved to: {args.output}")
            else:
                print(output)
        elif args.format == 'html':
            output = reporter.generate_html(results)
            output_path = args.output or 'vulnerability_report.html'
            Path(output_path).write_text(output)
            print(f"📄 HTML report saved to: {output_path}")
        
        # Exit with error code if vulnerabilities found
        # Java: System.exit(results.isEmpty() ? 0 : 1);
        sys.exit(1 if results else 0)
        
    except FileNotFoundError as e:
        print(f"❌ Error: File not found - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


# Python idiom: only run if this is the main script
# Java doesn't need this - main() is always the entry point
if __name__ == '__main__':
    main()