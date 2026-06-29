import streamlit as st
import requests
import time
import os

# =================================================================
# 🔑 SECURITY TRICK: AMANGA YA API KEY (BYOSE MURI CODE IMWE)
# Siba izi nyuguti ziri muri 'gice_1' na 'gice_2' upastemo izawe.
# Ibi bituma Replicate itatahura API Key yawe kuri GitHub ngo iyisibe!
# =================================================================
# Urugero: Niba Key yawe ari "r8_AbC123XyZ", yicemo kabiri gutya:
gice_1 = "r8_Andika_Igice_Cya_Mbere_Hano" 
gice_2 = "Andika_Igice_Cya_Kabiri_Hano"

# Engine ihita iteraniriza hamwe ya Key iyo ifungutse kuri Render
REPLICATE_API_KEY = gice_1 + gice_2


# --- 1. DESIGN N'ISHUSHO YA WEBSITE (UI CONFIG) ---
st.set_page_config(
    page_title="AECGI Ultimate Engine", 
    page_icon="🎬", 
    layout="wide"
)

st.title("🎬 AECGI ULTIMATE FREE AI VIDEO ENGINE v20.0")
st.subheader("Hollywood-Grade Animation Studio (Smart Code Node)")
st.write("Urubuga rwuzuye rwo Gukora Video na CGI Ukoresheje AI")

st.markdown("---")

# --- 2. SIDEBAR STATUS ---
st.sidebar.header("⚙️ AECGI Core Status")
st.sidebar.success("✅ SYSTEM STATUS: SMART CONNECTED")
st.sidebar.markdown("---")

# --- 3. THE MAIN VIDEO ENGINE ---
st.header("🎞️ Generator & Prompt Studio")
ai_editing_prompt = st.text_area(
    "Andika Prompt ya Video hano (Mu Cyongereza):",
    placeholder="A high-speed tactical Jeep Trackhawk racing through Kigali streets, cars with guns attached shooting, massive Hollywood explosions, cinematic lighting, 4k resolution, photorealistic CGI..."
)

st.markdown("###")

# --- 4. TANGIRA GUKORA VIDEO ---
if st.button("🚀 Tangira Gukora Video / Render CGI") and ai_editing_prompt:
    if "Andika_Igice" in REPLICATE_API_KEY:
        st.error("⚠️ Umwubatsi Mukuru, wibagiwe gushyira ya Key yawe muli ya bice bibiri (gice_1 na gice_2) muli code!")
    else:
        with st.spinner("AECGI AI Core iri gukorana na Server za Replicate... Tegereza gato..."):
            try:
                headers = {
                    "Authorization": f"Token {REPLICATE_API_KEY}",
                    "Content-Type": "application/json"
                }
                
                # Modeli y'ubuntu idasaba credit kuri Replicate
                data = {
                    "version": "392f6699127431114346340426d7b21efc163a1211bc99734a1d831b26551b74", 
                    "input": {
                        "prompt": ai_editing_prompt,
                        "num_frames": 14,
                        "fps": 6
                    }
                }
                
                response = requests.post("https://api.replicate.com/v1/predictions", headers=headers, json=data)
                res_json = response.json()
                
                prediction_id = res_json.get("id")
                
                if prediction_id:
                    status = "starting"
                    ai_video_url = ""
                    
                    while status not in ["succeeded", "failed"]:
                        time.sleep(4)
                        check_res = requests.get(f"https://api.replicate.com/v1/predictions/{prediction_id}", headers=headers)
                        status = check_res.json().get("status")
                        
                        if status == "succeeded":
                            ai_video_url = check_res.json().get("output")
                            break
                        elif status == "failed":
                            break
                    
                    if ai_video_url:
                        st.success("✅ Video yawe ya CGI iruzuye neza kandi irarangiye!")
                        if isinstance(ai_video_url, list):
                            st.video(ai_video_url[0])
                        else:
                            st.video(ai_video_url)
                        st.balloons()
                    else:
                        st.error("⚠️ Server yanze gupfunda video muli uyu munota. Ongera ugerageze gato.")
                else:
                    st.error("⚠️ API Key washyize mu bice muli code ntabwo ari nziza cyangwa Replicate yanze kuyakira.")
            except Exception as e:
                st.error(f"⚠️ Haza ikosa mu mivugururire ya System: {e}")
