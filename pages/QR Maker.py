import streamlit as st
import segno
from segno import helpers
from streamlit_option_menu import option_menu
from PIL import Image
import io
import base64

# App configuration with improved title and favicon
st.set_page_config(
    page_title="GRIT QR Studio",
    page_icon="🎨",
    layout="wide"
)

# CSS for styling the app
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E3A8A;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2563EB;
        margin-bottom: 0.5rem;
    }
    .download-btn {
        background-color: #10B981;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        text-decoration: none;
    }
    .stProgress > div > div > div {
        background-color: #60A5FA;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for navigation
with st.sidebar:
    app_pages = option_menu(
        "GRIT Studio", 
        ["QR Maker", "About"], 
        icons=["qr-code", "info-circle"], 
        menu_icon="brush"
    )
    
    st.sidebar.success("Select a Page above")
    st.sidebar.caption("We prioritize your privacy - no data is collected or processed")
    
    # Add social links in sidebar
    st.sidebar.markdown("### Connect with us")
    st.sidebar.markdown("[Linkedin](https://www.linkedin.com/in/samuel-o-momoh/) | [Twitter](https://twitter.com/griittyy) | [GitHub](https://github.com/GRIITTYY)")
    
    # App version
    st.sidebar.markdown("---")
    st.sidebar.caption("Version 1.1.0")

# QR Maker Page
if app_pages == "QR Maker":
    st.markdown("<div class='main-header'>QR Code Generator</div>", unsafe_allow_html=True)
    st.markdown("Create professional QR codes for various use cases. Customize colors, size, and content.")
    
    # Create tabs for different QR types
    qr_tabs = st.tabs(["Custom Link", "WiFi QR Code", "V-Card", "Text", "Email"])
    
    # Function to render settings alongside QR code
    def render_settings_and_qr(qr_object, qr_type, filename_prefix="qr_code"):
        # Create two columns - one for QR code, one for settings
        qr_col, settings_col = st.columns([2, 1])
        
        # Get settings values (default or from session state)
        colour = st.session_state.get(f"{qr_type}_colour", "#000000")
        background = st.session_state.get(f"{qr_type}_background", "#FFFFFF")
        size = st.session_state.get(f"{qr_type}_size", 10)
        border = st.session_state.get(f"{qr_type}_border", 2)
        error_correction = st.session_state.get(f"{qr_type}_error", "h")
        
        # Generate QR code with current settings
        filename = f"{filename_prefix}_temp.png"
        qr_object.save(
            filename,
            scale=size,
            border=border,
            light=background,
            dark=colour
        )
        
        # Display QR code in left column
        with qr_col:
            st.image(filename)
            
            # Download button
            with open(filename, "rb") as file:
                btn = st.download_button(
                    label="Download QR Image", 
                    data=file, 
                    file_name=f"{filename_prefix}.png", 
                    mime="image/png",
                    help="Save the QR code to your device"
                )
            
            # Get image in base64 for printing
            def get_image_base64(image_path):
                with open(image_path, "rb") as img_file:
                    return base64.b64encode(img_file.read()).decode()
            
        
        # Display settings in right column
        with settings_col:
            st.markdown("### Customize Your QR Code")
            
            # Basic settings
            new_colour = st.color_picker("QR dot color", colour, key=f"{qr_type}_color_picker")
            new_background = st.color_picker("Background color", background, key=f"{qr_type}_bg_picker")
            new_size = st.slider("Size", min_value=5, max_value=40, value=size, key=f"{qr_type}_size_slider")
            
            # Advanced settings expander
            with st.expander("Advanced Options", expanded=False):
                new_border = st.slider("Border size", min_value=0, max_value=10, value=border, key=f"{qr_type}_border_slider")
                new_error = st.selectbox(
                    "Error correction level",
                    options=["L", "M", "Q", "H"],
                    index=["l", "m", "q", "h"].index(error_correction.lower()),
                    help="Higher levels (H) allow QR to be readable even if partially damaged",
                    key=f"{qr_type}_error_select"
                )
                
            
            # Apply settings button
            if st.button("Apply Settings", key=f"{qr_type}_apply_btn"):
                # Store settings in session state
                st.session_state[f"{qr_type}_colour"] = new_colour
                st.session_state[f"{qr_type}_background"] = new_background
                st.session_state[f"{qr_type}_size"] = new_size
                st.session_state[f"{qr_type}_border"] = new_border
                st.session_state[f"{qr_type}_error"] = new_error.lower()
                st.rerun()  # Refresh to apply settings
    
    # 1. Custom Link Tab
    with qr_tabs[0]:
        st.markdown("<div class='sub-header'>Create a QR code for any URL</div>", unsafe_allow_html=True)
        text = st.text_input("Enter link here", placeholder="https://example.com", key="link_input")
        st.caption("*Press Enter to apply")
       
        if text:
            error_level = st.session_state.get("link_error", "h")
            qr_code = segno.make_qr(text, error=error_level)
            render_settings_and_qr(qr_code, "link", "link")
    
    # 2. WiFi QR Code Tab
    with qr_tabs[1]:
        st.markdown("<div class='sub-header'>Create a WiFi network QR code</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            ssid = st.text_input("Enter WiFi Name (SSID)", placeholder="Your WiFi Network", key="wifi_ssid")
        with col2:
            password = st.text_input("Enter Password", type="password", key="wifi_pass")
        with col3:
            security_type = st.selectbox("Select WiFi Security type", 
                                        options=["WEP", "WPA", "None"], 
                                        key="wifi_security")
        
        if ssid and (password or security_type == "None"):
            hide = st.radio("*WiFi network is hidden", 
                           options=["Yes", "No"], 
                           index=1, 
                           horizontal=True,
                           key="wifi_hidden")
            
            wifi = helpers.make_wifi(
                ssid=ssid, 
                password=password if password else None,
                security=None if security_type == "None" else security_type,
                hidden=True if hide == "Yes" else False
            )
            render_settings_and_qr(wifi, "wifi", "wifi")
    
    # 3. V-Card Tab
    with qr_tabs[2]:
        st.markdown("<div class='sub-header'>Create a contact information QR code</div>", unsafe_allow_html=True)
        
        # Use two columns for cleaner layout
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("Full Name", placeholder="John Doe", key="vcard_name")
            email = st.text_input("Email address", placeholder="john.doe@example.com", key="vcard_email")
            phone = st.text_input("Phone number", placeholder="+1 234 567 8901", key="vcard_phone")
            url = st.text_input("Website/Resume/Social Link", placeholder="https://linkedin.com/in/johndoe", key="vcard_url")
        
        with col2:
            org = st.text_input("Company name", placeholder="Acme Inc.", key="vcard_org")
            title = st.text_input("Job Title/Role", placeholder="Software Engineer", key="vcard_title")
            workphone = st.text_input("Work Phone Number", placeholder="+1 987 654 3210", key="vcard_workphone")
            country = st.text_input("Country", placeholder="United States", key="vcard_country")
        
        if first_name and phone:
            v_card = helpers.make_vcard(
                name="",
                displayname=first_name,
                email=email,
                phone=phone,
                url=url,
                country=country,
                org=org,
                title=title,
                workphone=workphone
            )
            render_settings_and_qr(v_card, "vcard", "vcard")
    
    # 4. Text Tab
    with qr_tabs[3]:
        st.markdown("<div class='sub-header'>Create a text QR code</div>", unsafe_allow_html=True)
        text_content = st.text_area("Enter your text content", 
                                   placeholder="Enter any text you want to encode in the QR code", 
                                   height=150,
                                   key="text_content")
        
        if text_content:
            error_level = st.session_state.get("text_error", "h")
            text_qr = segno.make_qr(text_content, error=error_level)
            render_settings_and_qr(text_qr, "text", "text")
    
    # 5. Email Tab
    with qr_tabs[4]:
        st.markdown("<div class='sub-header'>Create an email QR code</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            email_address = st.text_input("Recipient Email Address", 
                                         placeholder="recipient@example.com",
                                         key="email_recipient")
            subject = st.text_input("Email Subject", 
                                   placeholder="Meeting Invitation",
                                   key="email_subject")
        
        with col2:
            cc = st.text_input("CC (optional)", 
                              placeholder="colleague@example.com",
                              key="email_cc")
            bcc = st.text_input("BCC (optional)", 
                               placeholder="manager@example.com",
                               key="email_bcc")
        
        body = st.text_area("Email Body", 
                           placeholder="Write your email content here...", 
                           height=150,
                           key="email_body")
        
        if email_address:
            email_content = f"mailto:{email_address}"
            if cc:
                email_content += f"?cc={cc}"
            if subject:
                email_content += f"{'?' if '?' not in email_content else '&'}subject={subject}"
            if body:
                email_content += f"{'?' if '?' not in email_content else '&'}body={body}"
            if bcc:
                email_content += f"{'?' if '?' not in email_content else '&'}bcc={bcc}"
            
            error_level = st.session_state.get("email_error", "h")    
            email_qr = segno.make_qr(email_content, error=error_level)
            render_settings_and_qr(email_qr, "email", "email")

# About Page
elif app_pages == "About":
    st.markdown("<div class='main-header'>About QR Maker</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/QR_code_for_mobile_English_Wikipedia.svg/1200px-QR_code_for_mobile_English_Wikipedia.svg.png", width=200)
    
    with col2:
        st.markdown("""
        ### What is QR Maker?
        
        QR Maker is a powerful tool for creating customized QR codes for various purposes.
        Whether you need QR codes for your business, personal use, or promotional materials,
        our application gives you full control over the design and content of your QR codes.
        
        ### Features
        
        - **Multiple QR types**: Create QR codes for links, WiFi networks, contact cards, text, and emails
        - **Customization**: Change colors, sizes, and add logos to your QR codes
        - **Privacy-focused**: We don't collect or store your data
        
        ### How to Use
        
        1. Select the QR type you want to create
        2. Fill in the required information
        3. Customize the appearance using the side controls
        4. Download your QR code
        
        ### Contact Us
        
        For support or feedback, please email us at iammomohsamuel@gmail.com
        """)
    
    # FAQ section
    st.markdown("## Frequently Asked Questions")
    
    faq_1 = st.expander("What devices can scan these QR codes?")
    with faq_1:
        st.markdown("""
        Almost all modern smartphones can scan QR codes using the built-in camera app.
        For older phones, you might need to download a QR code scanner app from the App store or Play store.
        """)
    
    faq_2 = st.expander("Are there size limitations for QR codes?")
    with faq_2:
        st.markdown("""
        The physical size of a QR code doesn't impose strict limitations, but its resolution does.
        It’s important that the QR code is large enough to be easily scanned and has sufficient contrast. 
                    
        However, as more data is encoded in the QR code, it becomes more complex, which can affect its scanability. 
        Therefore, a balance between size, resolution, and data density should be maintained to ensure the QR code is both readable and functional.
        """)
    
    faq_3 = st.expander("What happens if a QR code is damaged?")
    with faq_3:
        st.markdown("""
        QR codes include error correction capabilities. 
        Depending on the level of error correction
        used (L, M, Q, or H), a QR code can still be readable even if 7-30% of it is damaged or obscured.
                    
        Our app uses the highest error correction level (H) by default.
        """)