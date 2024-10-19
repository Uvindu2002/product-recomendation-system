import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from datetime import datetime

# Step 1: Load Data
product_data = pd.read_csv("product_data_new.csv")  # Ensure the CSV contains necessary fields

# Step 2: Rating-Based Recommendation System
def get_top_rated_products(product_data, top_n=10):
    average_ratings = product_data.groupby(['Name','ReviewsCount','Brand','ImageURL'])['Rating'].mean().reset_index()
    top_rated_items = average_ratings.sort_values(by='Rating', ascending=False).head(top_n)
    return top_rated_items[['Name', 'Rating', 'ReviewsCount', 'Brand', 'ImageURL']]

# Step 3: Content-Based Recommendation System
def content_based_recommendations(product_data, item_name, top_n=10):
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix_content = tfidf_vectorizer.fit_transform(product_data['Tags'])
    
    item_index = product_data[product_data['Name'] == item_name].index[0]
    cosine_similarities_content = cosine_similarity(tfidf_matrix_content, tfidf_matrix_content)
    similar_items = sorted(list(enumerate(cosine_similarities_content[item_index])), key=lambda x: x[1], reverse=True)
    
    recommended_item_indices = [x[0] for x in similar_items[1:top_n+1]]
    return product_data.iloc[recommended_item_indices][['Name', 'ReviewsCount', 'Brand', 'ImageURL', 'Rating', 'Season']]

# Step 4: Collaborative Filtering Recommendation System
def collaborative_filtering_recommendations(product_data, target_user_id, top_n=10):
    user_item_matrix = product_data.pivot_table(index='user_id', columns='product_id', values='Rating', aggfunc='mean').fillna(0)
    user_similarity = cosine_similarity(user_item_matrix)
    
    target_user_index = user_item_matrix.index.get_loc(target_user_id)
    user_similarities = user_similarity[target_user_index]
    similar_users_indices = user_similarities.argsort()[::-1][1:]
    
    recommended_items = []
    for user_index in similar_users_indices:
        rated_by_similar_user = user_item_matrix.iloc[user_index]
        not_rated_by_target_user = (rated_by_similar_user == 0) & (user_item_matrix.iloc[target_user_index] == 0)
        recommended_items.extend(user_item_matrix.columns[not_rated_by_target_user][:top_n])
    
    return product_data[product_data['product_id'].isin(recommended_items)][['Name', 'ReviewsCount', 'Brand', 'ImageURL', 'Rating', 'Season']].head(top_n)

# Step 5: Hybrid Recommendation System
def hybrid_recommendations(product_data, target_user_id, item_name, top_n=10):
    content_based_rec = content_based_recommendations(product_data, item_name, top_n)
    collaborative_filtering_rec = collaborative_filtering_recommendations(product_data, target_user_id, top_n)
    
    hybrid_rec = pd.concat([content_based_rec, collaborative_filtering_rec]).drop_duplicates()
    hybrid_rec['Season'] = hybrid_rec['Season'].str.strip()

    current_month = datetime.now().month
    month_to_season = {12: 'Winter', 1: 'Winter', 2: 'Winter', 3: 'Spring', 4: 'Spring', 5: 'Spring', 6: 'Summer', 7: 'Summer', 8: 'Summer', 9: 'Autumn', 10: 'Autumn', 11: 'Autumn'}
    current_season = month_to_season[current_month]
    
    seasonal_hybrid_rec = hybrid_rec[hybrid_rec['Season'] == current_season]
    all_season_rec = hybrid_rec[hybrid_rec['Season'] == 'All Seasons']
    
    return pd.concat([seasonal_hybrid_rec, all_season_rec]).head(top_n)

# Example Usage
item_name = "OPI Nail Lacquer Polish .5oz/15mL - This Gown Needs A Crown NL U11"
target_user_id = 4
recommendation_products = hybrid_recommendations(product_data, target_user_id, item_name)

print("Hybrid Recommendations:")
print(recommendation_products)
