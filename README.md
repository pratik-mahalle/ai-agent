# Cloud-Native AI Agent

An intelligent AI agent designed to help developers and speakers in the cloud-native ecosystem by:

- 🔍 **Discovering Events**: Finding cloud-native events from Linux Foundation and CNCF
- 📝 **Generating Talk Proposals**: Creating compelling proposals using historical KubeCon data
- 🎓 **Scholarship Applications**: Assisting with scholarship application processes
- ✈️ **Travel Funding**: Helping with travel funding applications

## Features

### Event Discovery
- Scrapes Linux Foundation and CNCF websites for upcoming events
- Filters events by location, date, and relevance
- Provides event details, deadlines, and application requirements
- Caches results for improved performance

### Talk Proposal Generator
- Analyzes historical KubeCon talk data for trending topics
- Generates unique and compelling talk proposals
- Suggests optimal timing and track placement
- Provides speaker tips and best practices
- Includes learning objectives and talk outlines

### Scholarship Application Assistant
- Guides through scholarship application processes
- Helps craft compelling personal statements
- Tracks application deadlines and requirements
- Provides templates and examples
- Checks eligibility for different programs

### Travel Funding Assistant
- Identifies available travel funding opportunities
- Assists with budget planning and justification
- Helps with travel grant applications
- Tracks funding deadlines and requirements
- Provides cost estimation and optimization tips

## Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (for AI-powered features)
- Internet connection for web scraping

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-agent
   ```

2. **Run the setup script**
   ```bash
   python setup.py
   ```
   
   This will:
   - Install all required dependencies
   - Create necessary directories
   - Generate a `.env` file template
   - Run basic tests

3. **Configure your environment**
   ```bash
   # Edit the .env file and add your OpenAI API key
   nano .env
   ```

4. **Start the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8501`

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional - for enhanced scraping
LINUX_FOUNDATION_USERNAME=your_username
LINUX_FOUNDATION_PASSWORD=your_password
CNCF_USERNAME=your_username
CNCF_PASSWORD=your_password

# Application settings
DEBUG=False
LOG_LEVEL=INFO
REQUEST_TIMEOUT=30
MAX_RETRIES=3
CACHE_EXPIRY_HOURS=6
```

### Getting an OpenAI API Key

1. Visit [OpenAI's website](https://platform.openai.com/)
2. Create an account or sign in
3. Navigate to the API section
4. Generate a new API key
5. Add the key to your `.env` file

## Usage

### Web Interface

The main application provides a user-friendly web interface with the following sections:

#### Dashboard
- Overview of discovered events, generated proposals, and tracked applications
- Quick action buttons for common tasks
- Recent activity feed

#### Event Discovery
- Search and filter cloud-native events
- View event details, deadlines, and requirements
- Get recommendations based on your interests

#### Talk Proposals
- Generate compelling talk proposals
- Customize based on your expertise and target audience
- Get improvement suggestions and export options

#### Scholarships
- Browse available scholarship programs
- Check your eligibility
- Generate application materials

#### Travel Funding
- Find travel funding opportunities
- Estimate travel costs
- Generate funding applications

### Command Line Testing

Run the test script to verify functionality:

```bash
python test_agent.py
```

## Architecture

The agent is built with a modular architecture:

```
ai-agent/
├── agents/                 # Core AI agent modules
│   ├── base_agent.py      # Base agent class
│   ├── event_discovery.py # Event discovery agent
│   ├── proposal_generator.py # Proposal generation agent
│   ├── scholarship_assistant.py # Scholarship assistance agent
│   └── travel_funding_assistant.py # Travel funding agent
├── utils/                  # Utility functions
│   ├── web_scraper.py     # Web scraping utilities
│   ├── config.py          # Configuration management
│   └── data_processor.py  # Data processing utilities
├── data/                   # Sample data and templates
├── web/                    # Web interface components
├── app.py                  # Main Streamlit application
├── test_agent.py          # Test script
└── setup.py               # Setup script
```

## API Reference

### Event Discovery Agent

```python
from agents.event_discovery import EventDiscoveryAgent

agent = EventDiscoveryAgent()

# Discover events
result = await agent.discover_events({'type': 'discover'})

# Filter events
result = await agent.filter_events({
    'type': 'filter',
    'filters': {'location': 'San Francisco', 'min_relevance': 7.0}
})
```

### Proposal Generator Agent

```python
from agents.proposal_generator import ProposalGeneratorAgent

agent = ProposalGeneratorAgent()

# Generate proposal
result = await agent.generate_proposal({
    'type': 'generate',
    'topic': 'Kubernetes Operators in Production',
    'speaker_expertise': ['Kubernetes', 'DevOps'],
    'target_audience': 'intermediate',
    'talk_type': 'session'
})
```

### Scholarship Assistant Agent

```python
from agents.scholarship_assistant import ScholarshipAssistantAgent

agent = ScholarshipAssistantAgent()

# Check eligibility
result = await agent.check_eligibility({
    'type': 'check_eligibility',
    'applicant_info': {
        'is_student': True,
        'financial_need': True,
        'community_involvement': True
    }
})
```

### Travel Funding Assistant Agent

```python
from agents.travel_funding_assistant import TravelFundingAssistantAgent

agent = TravelFundingAssistantAgent()

# Estimate costs
result = await agent.estimate_costs({
    'type': 'estimate_costs',
    'event_details': {
        'location': 'San Francisco, CA',
        'duration_days': 3
    },
    'travel_preferences': {
        'departure_location': 'New York, NY',
        'accommodation': 'standard'
    }
})
```

## Development

### Setting up a development environment

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-agent
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install development dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

5. **Run tests**
   ```bash
   python -m pytest tests/
   ```

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests for new functionality
5. Run the test suite: `python -m pytest`
6. Commit your changes: `git commit -am 'Add feature'`
7. Push to the branch: `git push origin feature-name`
8. Submit a pull request

### Code Style

This project follows PEP 8 style guidelines. Use a linter like `flake8` or `black` to ensure code quality:

```bash
pip install flake8 black
flake8 .
black .
```

## Troubleshooting

### Common Issues

#### OpenAI API Key Error
```
Error: OPENAI_API_KEY environment variable is required
```
**Solution**: Add your OpenAI API key to the `.env` file

#### Import Errors
```
ModuleNotFoundError: No module named 'agents'
```
**Solution**: Make sure you're running from the project root directory

#### Web Scraping Issues
```
Error scraping website: Connection timeout
```
**Solution**: Check your internet connection and try again later

#### Streamlit Issues
```
Streamlit is not recognized as a command
```
**Solution**: Install Streamlit: `pip install streamlit`

### Getting Help

1. Check the [Issues](https://github.com/your-repo/issues) page
2. Search existing discussions
3. Create a new issue with:
   - Description of the problem
   - Steps to reproduce
   - Error messages
   - System information

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [OpenAI](https://openai.com/) for providing the GPT models
- [Streamlit](https://streamlit.io/) for the web framework
- [Linux Foundation](https://www.linuxfoundation.org/) and [CNCF](https://www.cncf.io/) for the cloud-native ecosystem
- The open-source community for inspiration and contributions

## Roadmap

- [ ] Database integration for persistent storage
- [ ] Advanced web scraping with authentication
- [ ] Integration with calendar systems
- [ ] Email notifications for deadlines
- [ ] Mobile app version
- [ ] Multi-language support
- [ ] Advanced analytics and reporting
- [ ] Integration with conference submission systems

## Support

If you find this project helpful, please consider:

- ⭐ Starring the repository
- 🐛 Reporting bugs
- 💡 Suggesting new features
- 🤝 Contributing code
- 📢 Sharing with the community

---

**Happy cloud-native development! 🚀** 