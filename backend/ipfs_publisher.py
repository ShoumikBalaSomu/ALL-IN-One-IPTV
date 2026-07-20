import requests
import os

# --- Decentralized Off-Grid IPFS Publisher ---
# Assumes you have a local IPFS daemon (Kubo) running on port 5001, 
# or you can point this to a generic pinning API like Pinata.

IPFS_API_URL = "http://127.0.0.1:5001/api/v0"

def publish_to_ipfs(file_path: str):
    """
    Pins the generated M3U file to the InterPlanetary File System (IPFS).
    Returns the immutable CID hash.
    """
    if not os.path.exists(file_path):
        return None
        
    print(f"IPFSPublisher: Uploading {file_path} to decentralized network...")
    
    with open(file_path, 'rb') as f:
        files = {'file': f}
        try:
            # Add to IPFS
            res = requests.post(f"{IPFS_API_URL}/add", files=files, timeout=10)
            res.raise_for_status()
            
            cid = res.json()["Hash"]
            print(f"IPFSPublisher: Successfully pinned! CID: {cid}")
            
            # Optional: Publish to IPNS to keep a static address
            # update_ipns(cid)
            
            return cid
        except Exception as e:
            print(f"IPFSPublisher: Failed to connect to IPFS node - {e}")
            return None

def update_ipns(cid: str):
    """
    Updates the IPNS pointer so clients don't need to update their hardcoded URLs.
    """
    try:
        res = requests.post(f"{IPFS_API_URL}/name/publish?arg={cid}")
        ipns_hash = res.json()["Name"]
        print(f"IPFSPublisher: IPNS Updated -> k51qzi5uqu5d... -> points to {cid}")
    except Exception as e:
        print(f"IPFSPublisher: Failed to update IPNS - {e}")

if __name__ == "__main__":
    # Test execution
    mock_file = "output/checked_combined_by_country.m3u"
    # Create dummy file if missing just for test execution
    if not os.path.exists("output"): os.makedirs("output")
    with open(mock_file, "w") as f: f.write("#EXTM3U\n")
    
    publish_to_ipfs(mock_file)
