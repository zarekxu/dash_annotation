from atlassian import Confluence

# Connect to Confluence
confluence = Confluence(
    url='https://bobojixu.atlassian.net/',
    username="bobojixu@gmail.com",
    password=''  # It's recommended to use API tokens instead of passwords
)

# Define the page title and space key
page_title = "Test Document 1"
space_key = "~7120209e13d0a704fa4e438d98c0a30bf75e3e"  # Optional if the page title is unique across the instance

try:
    space_info = confluence.get_space(space_key, expand='description.plain,homepage')
    print("Space Info:", space_info)
except Exception as e:
    print("Failed to retrieve page:", str(e))
