import streamlit as st
import html
import re
import pyperclip
from st_social_media_links import SocialMediaIcons

# Define Unicode mapping functions
def to_bold(text):
    bold_offset_upper = 0x1D400 - ord('A')
    bold_offset_lower = 0x1D41A - ord('a')
    return ''.join(
        chr(ord(char) + bold_offset_upper) if 'A' <= char <= 'Z' else
        chr(ord(char) + bold_offset_lower) if 'a' <= char <= 'z' else char
        for char in text
    )

def to_italic(text):
    italic_offset_upper = 0x1D434 - ord('A')
    italic_offset_lower = 0x1D44E - ord('a')
    return ''.join(
        chr(ord(char) + italic_offset_upper) if 'A' <= char <= 'Z' else
        chr(ord(char) + italic_offset_lower) if 'a' <= char <= 'z' else char
        for char in text
    )

def to_underline(text):
    return ''.join(f"{char}\u0332" for char in text)  # Underline using combining low line

def to_bullet_list(items):
    bullet = "\u2022"
    return '\n'.join(f"{bullet} {item}" for item in items)

def to_enumerated_list(items):
    return '\n'.join(f"{index + 1}. {item}" for index, item in enumerate(items))

def markup_to_unicode(input_text):
    decoded_text = html.unescape(input_text)

    def style_replacer(match):
        symbol, content = match.groups()
        if symbol == "*":
            return to_bold(content)
        elif symbol == "_":
            return to_italic(content)
        elif symbol == "~":
            return f"\u0336{''.join([c + '\u0336' for c in content])}"  # Strikethrough
        elif symbol == "^":
            return to_underline(content)  # Underline
        return content

    styled_text = re.sub(r"([*_~^])(.+?)\1", style_replacer, decoded_text)

    bullet_list_pattern = re.compile(r"(?:^|\n)- (.+?)(?=$|\n)")
    styled_text = bullet_list_pattern.sub(lambda m: f"\n• {m.group(1)}", styled_text)

    enumerated_list_pattern = re.compile(r"(?:^|\n)(\d+)\. (.+?)(?=$|\n)")
    styled_text = enumerated_list_pattern.sub(lambda m: f"\n{m.group(1)}. {m.group(2)}", styled_text)

    return styled_text

def main():
    # Streamlit App
    st.set_page_config(layout="wide", page_title="Beautify My LinkedIn Post", page_icon="Beautiful_Linkedin.png")

    # Main Container
    c1,main_col,c2 = st.columns([1, 6, 1])

    with main_col:
        st.title("Beautify My LinkedIn Post")
        st.markdown("Created with 💪 and ❤️ by [Rodrigo Ferreira](https://www.linkedin.com/in/rodrigoavf/)")
        social_media_links = [
            "https://www.github.com/rodrigoavf",
            "https://www.linkedin.com/in/rodrigoavf/"
        ]


        colors = ["White", None]
        social_media_icons = SocialMediaIcons(social_media_links, colors)

        social_media_icons.render(justify_content="start")

        st.divider()

        col0, col1, col2 = st.columns([1,2,2])  # Adjust column width to balance layout
        
        with col0:
            # Instructions for Markdown Formatting
            st.markdown(
                """
                **Instructions**
                - Use `*text*` for **bold**.
                - Use `_text_` for *italic*.
                - Use `~text~` for ~~strikethrough~~.
                - Use `^text^` for <u>underline</u>.
                - Use `- Item` for bullet lists.
                - Use `1. Item` for enumerated lists.
                """,
                unsafe_allow_html=True
            )

        with col1:
            st.markdown("**Your post's text below**")
            markdown_text = st.text_area("Markdown Text:", height=300, key="markdown_input", label_visibility="collapsed", placeholder="Enter your post text here, use the markdowns shown on the left to format your text.")
            if st.button("Convert"):
                unicode_text = markup_to_unicode(markdown_text)
                # st.text_area("Converted Unicode Text:", value=unicode_text, height=300, disabled=True, key="unicode_output")

        with col2:
            unicode_text = markup_to_unicode(markdown_text)
            st.markdown("**Beautified version of your post**")
            st.text_area("Converted Unicode Text:", value=unicode_text, height=300, disabled=True, key="unicode_output", label_visibility="collapsed", placeholder="Your beautified post will appear here.")
            # Copy Button
            if st.button("Copy to Clipboard"):
                pyperclip.copy(unicode_text)
                st.success("Converted text copied to clipboard!")

        # Before and After Preview
        st.markdown("### Before and After")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h5 style='text-align: center;'>Lame post, before beautifier</h5>", unsafe_allow_html=True)
        with col2:
            st.markdown("<h5 style='text-align: center;'>Awesome post, with beautifier</h5>", unsafe_allow_html=True)
        st.image("Before_After.png", output_format="PNG")

if __name__ == "__main__":
    main()