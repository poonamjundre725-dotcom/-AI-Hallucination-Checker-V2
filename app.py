import streamlit as st

from llm import ask_gemini
from verifier import verify_answer
from fact_checker import get_combined_evidence

st.set_page_config(
    page_title="AI Hallucination Checker",
    page_icon="🤖"
)

st.title("🤖 AI Hallucination Checker")

st.write(
    "Compare AI-generated answers with trusted web sources to detect possible hallucinations."
)

question = st.text_input("Enter your question")

if st.button("Check Answer"):

    if question:

        with st.spinner("Generating AI answer..."):
            ai_answer = ask_gemini(question)

        st.subheader("🤖 AI Answer")
        st.write(ai_answer)

        with st.spinner("Collecting evidence..."):
            evidence = get_combined_evidence(question)

        with st.spinner("Checking hallucination..."):
            result = verify_answer(
                question,
                ai_answer,
                evidence
            )

        confidence = result["confidence"]
        risk = result["risk"]
        verdict = result["verdict"]
        reason = result["reason"]

        st.subheader("📊 Verification Result")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Confidence Score",
                f"{confidence}%"
            )

        with col2:
            st.metric(
                "Hallucination Risk",
                f"{risk}%"
            )

        st.progress(float(confidence) / 100)

        st.subheader("📌 Final Verdict")

        if verdict == "No Hallucination":
            st.success("✅ No Hallucination")

        elif verdict == "Partial Hallucination":
            st.warning("⚠️ Partial Hallucination")

        else:
            st.error("❌ Hallucination Detected")

        st.write(f"**Confidence:** {confidence}%")
        st.write(f"**Hallucination Risk:** {risk}%")
        st.write(f"**Verdict:** {verdict}")
        st.write(f"**Reason:** {reason}")

        with st.expander("📚 Verification Sources"):

            if evidence:
                st.write(evidence[:10000])

            else:
                st.warning(
                    "No trusted evidence found."
                )

    else:
        st.warning("Please enter a question.")