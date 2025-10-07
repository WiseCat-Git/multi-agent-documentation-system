from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",  # More cost-effective than gpt-4
    temperature=0.7,
    api_key=os.getenv('OPENAI_API_KEY')
)

# Initialize tools
search_tool = SerperDevTool(api_key=os.getenv('SERPER_API_KEY'))
scrape_tool = ScrapeWebsiteTool()

def create_agents():
    """Create the four specialized agents"""
    
    # 1. Researcher Agent
    researcher = Agent(
        role='Technical Researcher',
        goal='Gather comprehensive information about the topic, analyze context, and identify key features and dimensions',
        backstory="""You are an expert researcher with a keen eye for detail. 
        You excel at finding relevant information, understanding technical concepts, 
        and breaking down complex topics into structured insights. You always verify 
        your sources and provide context-rich analysis.""",
        tools=[search_tool, scrape_tool],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )
    
    # 2. Documentation Specialist Agent
    documentation_specialist = Agent(
        role='Senior Documentation Specialist',
        goal='Transform research findings into clear, structured, and professional technical documentation',
        backstory="""You are a seasoned technical writer with 10+ years of experience. 
        You know how to take complex information and make it accessible without losing 
        technical accuracy. Your documentation is known for its clarity, organization, 
        and completeness. You follow best practices in technical writing.""",
        llm=llm,
        verbose=True,
        allow_delegation=False
    )
    
    # 3. Quality Reviewer Agent
    reviewer = Agent(
        role='Quality Assurance Reviewer',
        goal='Review documentation for accuracy, completeness, clarity, and adherence to standards',
        backstory="""You are a meticulous reviewer with an eye for inconsistencies and gaps. 
        You ensure that documentation meets the highest standards of quality, is technically 
        accurate, and provides real value to readers. You catch errors others miss and 
        suggest meaningful improvements.""",
        llm=llm,
        verbose=True,
        allow_delegation=False
    )
    
    # 4. Training Material Creator Agent
    trainer = Agent(
        role='Training & Onboarding Specialist',
        goal='Convert technical documentation into engaging, easy-to-understand training materials',
        backstory="""You are an expert educator who excels at creating onboarding and 
        training content. You understand different learning styles and know how to present 
        information in ways that stick. You create materials that help new team members 
        quickly become productive.""",
        llm=llm,
        verbose=True,
        allow_delegation=False
    )
    
    return researcher, documentation_specialist, reviewer, trainer

def create_tasks(agents, inputs):
    """Create the sequential tasks for the crew"""
    
    researcher, doc_specialist, reviewer, trainer = agents
    
    # Task 1: Research
    research_task = Task(
        description=f"""Research and analyze the following topic:
        
        Topic: {inputs['topic']}
        Template Type: {inputs['template']}
        Additional Context: {inputs['content']}
        
        Your objectives:
        1. Understand the core concepts and context
        2. Identify key features, dimensions, or components
        3. Gather relevant technical details and best practices
        4. Organize findings in a structured format
        
        Provide a comprehensive research summary with all relevant information.""",
        expected_output="""A detailed research report containing:
        - Executive summary of the topic
        - Key features and dimensions identified
        - Technical details and context
        - Relevant sources and references
        - Structured findings ready for documentation""",
        agent=researcher
    )
    
    # Task 2: Documentation Creation
    documentation_task = Task(
        description=f"""Using the research findings, create professional {inputs['template']} documentation.
        
        Requirements:
        1. Use clear, professional language
        2. Follow {inputs['template']} structure and conventions
        3. Include all essential sections
        4. Add examples where appropriate
        5. Ensure logical flow and organization
        
        Create comprehensive documentation that serves as the definitive reference.""",
        expected_output=f"""Complete {inputs['template']} with:
        - Proper structure and formatting
        - All essential sections filled out
        - Clear explanations and examples
        - Professional language throughout
        - Ready for review""",
        agent=doc_specialist,
        context=[research_task]
    )
    
    # Task 3: Quality Review
    review_task = Task(
        description="""Review the documentation thoroughly for:
        
        1. Technical accuracy
        2. Completeness (no missing sections)
        3. Clarity and readability
        4. Consistency in terminology and style
        5. Proper grammar and formatting
        
        Provide the FINAL REVIEWED VERSION with all improvements incorporated.""",
        expected_output="""Final reviewed documentation with:
        - All errors corrected
        - Improvements implemented
        - Consistent formatting
        - Professional quality
        - Ready for publication
        
        IMPORTANT: Output the complete, final version of the documentation, not just a review report.""",
        agent=reviewer,
        context=[research_task, documentation_task]
    )
    
    # Task 4: Training Material Creation
    training_task = Task(
        description="""Transform the reviewed documentation into training/onboarding materials.
        
        Create:
        1. Quick start guide
        2. Key takeaways (bullet points)
        3. Common scenarios or use cases
        4. Tips and best practices
        5. FAQ section
        
        Make it engaging and easy to learn from.""",
        expected_output="""Training materials including:
        - Quick start guide (step-by-step)
        - Key takeaways summary
        - Practical examples and scenarios
        - Tips and best practices
        - FAQ with common questions
        - Formatted for easy learning""",
        agent=trainer,
        context=[review_task]
    )
    
    return [research_task, documentation_task, review_task, training_task]

def generate_documentation(topic, template, content):
    """Main function to orchestrate the multi-agent documentation generation"""
    
    # Create agents
    agents = create_agents()
    
    # Prepare inputs
    inputs = {
        'topic': topic,
        'template': template,
        'content': content
    }
    
    # Create tasks
    tasks = create_tasks(agents, inputs)
    
    # Create crew
    crew = Crew(
        agents=list(agents),
        tasks=tasks,
        process=Process.sequential,  # Tasks execute in order
        verbose=True
    )
    
    # Execute the crew
    result = crew.kickoff()
    
    return result

# For standalone testing
if __name__ == "__main__":
    test_topic = "Python Best Practices for Data Science Projects"
    test_template = "Technical Documentation"
    test_content = "Focus on code organization, version control, and reproducibility"
    
    result = generate_documentation(test_topic, test_template, test_content)
    print("\n" + "="*80)
    print("FINAL OUTPUT:")
    print("="*80)
    print(result)