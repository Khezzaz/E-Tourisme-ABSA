# ===== services/plot_generator.py =====
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, List
import os

class PlotGenerator:
    def __init__(self):
        plt.style.use('default')
        
        # Restaurant aspects in English
        self.restaurant_aspects = {
            'food': ['food', 'meal', 'dish', 'taste', 'flavor', 'cuisine'],
            'service': ['service', 'waiter', 'staff', 'server', 'waitress'],
            'ambiance': ['ambiance', 'atmosphere', 'decor', 'music', 'environment'],
            'price': ['price', 'cost', 'expensive', 'cheap', 'value', 'money'],
            'location': ['location', 'place', 'parking', 'access', 'area']
        }
    
    def generate_dashboard(self, analysis_results: List[Dict], session_id: str) -> Dict[str, str]:
        plots = {}
        
        # Prepare data
        all_aspects = []
        for result in analysis_results:
            all_aspects.extend(result.get("aspects", []))
        
        if not all_aspects:
            return plots
            
        df = pd.DataFrame(all_aspects)
        
        # Generate 4 plots
        plots['sentiment_dist'] = self._plot_sentiment_distribution(df, session_id)
        plots['top_aspects'] = self._plot_top_aspects(df, session_id)
        plots['category_heatmap'] = self._plot_category_heatmap(df, session_id)
        plots['satisfaction'] = self._plot_satisfaction_score(df, session_id)
        
        return plots
    
    def _plot_sentiment_distribution(self, df: pd.DataFrame, session_id: str) -> str:
        plt.figure(figsize=(10, 6))
        
        counts = df['polarity'].value_counts()
        colors = {'positive': 'green', 'negative': 'red', 'neutral': 'gray'}
        
        bars = plt.bar(counts.index, counts.values, 
                      color=[colors.get(x, 'gray') for x in counts.index])
        
        plt.title('Sentiment Distribution', fontsize=16, fontweight='bold')
        plt.xlabel('Sentiment')
        plt.ylabel('Count')
        
        # Add values on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{int(height)}', ha='center', va='bottom')
        
        plt.tight_layout()
        path = f"static/plots/sentiment_dist_{session_id}.png"
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()
        return path
    
    def _plot_top_aspects(self, df: pd.DataFrame, session_id: str) -> str:
        plt.figure(figsize=(12, 8))
        
        top_aspects = df['aspect'].value_counts().head(10)
        
        plt.barh(range(len(top_aspects)), top_aspects.values, color='skyblue')
        plt.yticks(range(len(top_aspects)), top_aspects.index)
        plt.title('Top 10 Most Mentioned Aspects', fontsize=16, fontweight='bold')
        plt.xlabel('Count')
        
        plt.tight_layout()
        path = f"static/plots/top_aspects_{session_id}.png"
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()
        return path
    
    def _plot_category_heatmap(self, df: pd.DataFrame, session_id: str) -> str:
        plt.figure(figsize=(10, 6))
        
        # Categorize aspects
        df['category'] = df['aspect'].apply(self._categorize_aspect)
        
        # Create heatmap data
        heatmap_data = pd.crosstab(df['category'], df['polarity'])
        
        sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='RdYlGn')
        plt.title('Sentiment by Aspect Category', fontsize=16, fontweight='bold')
        plt.xlabel('Sentiment')
        plt.ylabel('Category')
        
        plt.tight_layout()
        path = f"static/plots/heatmap_{session_id}.png"
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()
        return path
    
    def _plot_satisfaction_score(self, df: pd.DataFrame, session_id: str) -> str:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Calculate satisfaction score
        counts = df['polarity'].value_counts()
        total = len(df)
        
        positive_ratio = counts.get('positive', 0) / total
        neutral_ratio = counts.get('neutral', 0) / total
        satisfaction_score = (positive_ratio * 100 + neutral_ratio * 50)
        
        # Gauge chart (simplified)
        ax1.pie([satisfaction_score, 100-satisfaction_score], 
               colors=['green', 'lightgray'],
               startangle=90, counterclock=False)
        ax1.text(0, 0, f'{satisfaction_score:.1f}%', 
                ha='center', va='center', fontsize=20, fontweight='bold')
        ax1.set_title('Satisfaction Score', fontsize=14, fontweight='bold')
        
        # Pie chart
        sizes = [counts.get('positive', 0), counts.get('neutral', 0), counts.get('negative', 0)]
        labels = ['Positive', 'Neutral', 'Negative']
        colors = ['green', 'gray', 'red']
        
        ax2.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
        ax2.set_title('Sentiment Distribution', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        path = f"static/plots/satisfaction_{session_id}.png"
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()
        return path
    
    def _categorize_aspect(self, aspect: str) -> str:
        aspect_lower = aspect.lower()
        for category, keywords in self.restaurant_aspects.items():
            if any(keyword in aspect_lower for keyword in keywords):
                return category
        return 'other'