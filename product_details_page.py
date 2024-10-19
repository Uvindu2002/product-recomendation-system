import streamlit as st
import pandas as pd

# Load dataset (assuming the file is in the same directory)
@st.cache_data
def load_data():
    return pd.read_csv('product_data_new.csv')

# Define a function for the product details page
def product_details_page():
    # Load the product data
    data = load_data()

    # Check if a product ID has been selected
    if 'selected_product_id' not in st.session_state:
        st.error("No product selected. Please go back to the products page.")
        return

    # Get the selected product ID
    product_id = st.session_state.selected_product_id

    # Filter the product data for the selected product ID
    product = data[data['product_id'] == product_id]

    # Check if the product exists
    if product.empty:
        st.error(f"No product found with ID: {product_id}")
        return

    # Get the first matching product details
    product = product.iloc[0]

    # Set the title for the page
    st.title(f"Product Details - {product['Name']}")

    # Create a layout with columns for the image and details
    col1, col2 = st.columns([1, 2])

    # Display product image
    with col1:
        st.image(product['ImageURL'], use_column_width='always')

    # Display product details in the second column
    with col2:
        st.header(product['Name'])
        st.subheader(f"Brand: {product['Brand']}")
        st.markdown(f"**Rating:** {product['Rating']}/5")
        st.markdown(f"**Description:**")
        st.write(product['Description'])

        # Add a button for adding to favorites or cart
        if st.button("Add to Cart"):
            st.success(f"{product['Name']} has been added to your cart!")
        
        # Add a button for sharing the product link
        st.markdown("---")
        st.write("Share this product:")
        share_url = f"https://example.com/products/{product_id}"  # Replace with your actual URL structure
        st.text_input("Copy this link:", value=share_url, disabled=True)

    # Add a separator line
    st.markdown("---")

    # Optional: Related products or recommendations section
    st.subheader("Related Products")

    # Filter related products based on category or brand
    related_products = data[
        (data['Category'] == product['Category']) | (data['Brand'] == product['Brand'])
    ]

    # Remove the current product from the related products
    related_products = related_products[related_products['product_id'] != product_id]

    # Limit to the first 5 related products
    related_products = related_products.head(5)

    # Display related products
    if not related_products.empty:
        for index, related_product in related_products.iterrows():
            st.write(f"**{related_product['Name']}**")
            st.markdown(f"Brand: {related_product['Brand']}, Rating: {related_product['Rating']}/5")
            st.image(related_product['ImageURL'], width=100)

            # Use a button to redirect to the details page of the related product
            # Combine the index with the product ID for a unique key
            if st.button(f"View Details", key=f"view_details_{index}_{str(related_product['product_id'])}"):
                st.session_state.selected_product_id = related_product['product_id']  # Set the selected product ID
                st.experimental_rerun()  # Rerun the app to show the details of the selected product
            
            st.markdown("---")  # Separator for related products
    else:
        st.write("No related products found.")

    # Additional styling or layout options can be added as per your design preferences
