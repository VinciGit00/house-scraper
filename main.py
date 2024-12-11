import streamlit as st
from scrapegraph_py import Client
from scrapegraph_py.logger import sgai_logger

# Configure logging
sgai_logger.set_logging(level="INFO")

websites = [
    "zillow",
    "realtor",
    "homes.com",
    "trulia"
]

def get_website_url(website, city, state):
    """Generate website URL based on selected city and state"""
    urls = {
        "zillow": f"https://www.zillow.com/homes/for_sale/{city},-{state}_rb/",
        "realtor": f"https://www.realtor.com/realestateandhomes-search/{city}_{state}",
        "homes.com": f"https://www.homes.com/{city.lower()}-{state.lower()}/",
        "trulia": f"https://www.trulia.com/{state}/{city}/"
    }
    return urls.get(website)

def scrape_website(url, api_key):
    """Scrape website data using ScapeGraph"""
    try:
        # Initialize ScapeGraph client
        client = Client(api_key=api_key)
        
        # Define scraping prompt based on real estate data
        prompt = """
        Extract the following information:
        - Current property listings
        - Price ranges
        - Number of bedrooms/bathrooms
        - Square footage
        - Property types available
        """
        
        # Make scraping request
        response = client.smartscraper(
            website_url=url,
            user_prompt=prompt
        )
        
        client.close()
        return response['result']
        
    except Exception as e:
        return f"Error scraping website: {str(e)}"

def main():
    st.title("🏡Real Estate Website Directory")
    
    # API Key input
    api_key = st.text_input("Enter your ScapeGraph API Key", type="password")
    
    # Location inputs
    col1, col2 = st.columns(2)
    with col1:
        city = st.text_input("Enter City", value="Miami")
    with col2:
        state = st.text_input("Enter State (2-letter code)", value="FL", max_chars=2)
    
    # Create a sidebar menu
    selected_website = st.sidebar.selectbox(
        "Choose a real estate website",
        websites,
        key="website_selector"
    )
    
    # Main content area
    st.header(f"You selected: {selected_website.title()}")
    
    # Generate URL based on selected location
    website_url = get_website_url(selected_website, city, state)
    
    if website_url:
        st.markdown(f"[Visit {selected_website.title()}]({website_url})")
        
        # Add scraping button with unique key
        if st.button("Scrape Website Data", key="scrape_button") and api_key:
            with st.spinner("Scraping website data..."):
                result = scrape_website(website_url, api_key)
                st.json(result)
        elif not api_key:
            st.warning("Please enter your ScapeGraph API key first")

if __name__ == "__main__":
    main()
