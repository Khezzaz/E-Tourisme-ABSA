# ===== utils/file_utils.py =====
import pandas as pd
import io
import base64

def process_csv_file(file_contents: bytes, comment_column: str = "comment") -> pd.DataFrame:
    try:
        # Try different encodings
        for encoding in ['utf-8', 'latin-1', 'cp1252']:
            try:
                df = pd.read_csv(io.StringIO(file_contents.decode(encoding)))
                
                # Check if comment column exists
                if comment_column not in df.columns:
                    # Try to find similar column
                    possible_cols = [col for col in df.columns 
                                   if any(word in col.lower() 
                                        for word in ['comment', 'review', 'text'])]
                    
                    if possible_cols:
                        df = df.rename(columns={possible_cols[0]: comment_column})
                    else:
                        raise ValueError(f"Column '{comment_column}' not found")
                
                # Clean data
                df = df.dropna(subset=[comment_column])
                df[comment_column] = df[comment_column].astype(str)
                
                return df
                
            except UnicodeDecodeError:
                continue
        
        raise ValueError("Cannot decode CSV file")
        
    except Exception as e:
        print(f"Error processing CSV: {e}")
        return pd.DataFrame()

def encode_image_to_base64(image_path: str) -> str:
    try:
        with open(image_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode('utf-8')
            return f"data:image/png;base64,{encoded}"
    except Exception as e:
        print(f"Error encoding image: {e}")
        return ""