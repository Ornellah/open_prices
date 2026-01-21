"""
Streamlit main app page for OpenPrices.

Displays the dashboard homepage with sections describing the available
visualizations (top products/categories, sales by currency/country, trends,
and store sales).
"""

import streamlit as st

st.set_page_config(page_title="Dashboard", layout="wide")

st.title("Accueil")

st.markdown(
    """
    <div style="font-size:28px; margin-bottom:40px; font-weight:600;">
        Description des dashboards disponibles
    </div>

    <div style="display:block;">
        <div style="display:inline-block; border: 3px solid gray;  
        border-radius: 20px; padding: 15px; margin-bottom: 20px;">
            <div style="font-size:22px; font-weight:700; margin-bottom:10px;">
                Ventes par devise
            </div>
            <div style="font-size:18px; line-height:1.5;">
                <ul style="margin:0; padding-left:18px;">
                    <li><b>Top N devises (produits)</b> : 
                    devises les plus vendues (produits)</li>
                    <li><b>Toutes les devises (produits)</b> : 
                    toutes les devises (produits)</li>
                    <li><b>Top N devises (catégories)</b> : 
                    devises les plus vendues (catégories)</li>
                    <li><b>Toutes les devises (catégories)</b> : 
                    toutes les devises (catégories)</li>
                </ul>
            </div>
        </div>
    </div>

    <div style="display:block;">
        <div style="display:inline-block; border: 3px solid gray;  
        border-radius: 20px; padding: 15px; margin-bottom: 20px;">
            <div style="font-size:22px; font-weight:700; margin-bottom:10px;">
                Ventes par pays
            </div>
            <div style="font-size:18px; line-height:1.5;">
                <ul style="margin:0; padding-left:18px;">
                    <li><b>Top N pays (produits)</b> : 
                    pays avec le plus de ventes (produits)</li>
                    <li><b>Tous les pays (produits)</b> : 
                    tous les pays (produits)</li>
                    <li><b>Top N pays (catégories)</b> : 
                    pays avec le plus de ventes (catégories)</li>
                    <li><b>Tous les pays (catégories)</b> : 
                    tous les pays (catégories)</li>
                </ul>
            </div>
        </div>
    </div>

    <div style="display:block;">
        <div style="display:inline-block; border: 3px solid gray;  
        border-radius: 20px; padding: 15px; margin-bottom: 20px;">
            <div style="font-size:22px; font-weight:700; margin-bottom:10px;">
                Tendance de vente par devise
            </div>
            <div style="font-size:18px; line-height:1.5;">
                <ul style="margin:0; padding-left:18px;">
                    <li><b>Un produit</b> : 
                    évolution mensuelle d’un produit</li>
                    <li><b>Plusieurs produits</b> : 
                    évolution mensuelle de plusieurs produits</li>
                    <li><b>Une catégorie</b> : 
                    évolution mensuelle d’une catégorie</li>
                    <li><b>Plusieurs catégories</b> : 
                    évolution mensuelle de plusieurs catégories</li>
                </ul>
            </div>
        </div>
    </div>

    <div style="display:block;">
        <div style="display:inline-block; border: 3px solid gray;  
        border-radius: 20px; padding: 15px; margin-bottom: 20px;">
            <div style="font-size:22px; font-weight:700; margin-bottom:10px;">
                Tendance de vente par pays
            </div>
            <div style="font-size:18px; line-height:1.5;">
                <ul style="margin:0; padding-left:18px;">
                    <li><b>Un produit</b> : 
                    évolution mensuelle d’un produit</li>
                    <li><b>Plusieurs produits</b> : 
                    évolution mensuelle de plusieurs produits</li>
                    <li><b>Une catégorie</b> : 
                    évolution mensuelle d’une catégorie</li>
                    <li><b>Plusieurs catégories</b> : 
                    évolution mensuelle de plusieurs catégories</li>
                </ul>
            </div>
        </div>
    </div>

    <div style="display:block;">
        <div style="display:inline-block; border: 3px solid gray;  
        border-radius: 20px; padding: 15px; margin-bottom: 20px;">
            <div style="font-size:22px; font-weight:700; margin-bottom:10px;">
                Ventes par magasin
            </div>
            <div style="font-size:18px; line-height:1.5;">
                <ul style="margin:0; padding-left:18px;">
                    <li><b>Top N magasins (produits)</b> : 
                    magasins avec le plus de ventes (produits)</li>
                    <li><b>Tous les magasins (produits)</b> : 
                    tous les magasins (produits)</li>
                    <li><b>Top N magasins (catégories)</b> : 
                    magasins avec le plus de ventes (catégories)</li>
                    <li><b>Tous les magasins (catégories)</b> : 
                    tous les magasins (catégories)</li>
                </ul>
            </div>
        </div>
    </div>

    <div style="display:block;">
        <div style="display:inline-block; border: 3px solid gray;  
        border-radius: 20px; padding: 15px; margin-bottom: 20px;">
            <div style="font-size:22px; font-weight:700; margin-bottom:10px;">
                Ventes annuelles par produit et catégorie
            </div>
            <div style="font-size:18px; line-height:1.5;">
                <ul style="margin:0; padding-left:18px;">
                    <li><b>Top N produits</b> : 
                    meilleurs produits par devise</li>
                    <li><b>Tous les produits par devise</b> : 
                    tous les produits par devise</li>
                    <li><b>Top N catégories</b> : 
                    meilleures catégories par devise</li>
                    <li><b>Toutes les catégories par devise</b> : 
                    toutes les catégories par devise</li>
                </ul>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
