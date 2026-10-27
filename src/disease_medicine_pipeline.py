from disease_prediction import predict_disease
from medicine_pipeline import get_medicine_with_safety
from input_validation import validate_symptoms


# ============================================================
# COMPLETE HEALTHCARE DECISION-SUPPORT PIPELINE
# ============================================================

def run_healthcare_pipeline(symptoms):
    """
    Complete academic healthcare decision-support pipeline.

    Flow:
        Symptoms
            ↓
        Input Validation
            ↓
        Disease Prediction
            ↓
        Model Confidence
            ↓
        XAI Explanation
            ↓
        Medicine Information Retrieval
            ↓
        Safety Information

    This system does not diagnose or prescribe medicines.
    """

    # --------------------------------------------------------
    # STEP 1: VALIDATE SYMPTOMS
    # --------------------------------------------------------

    validation_result = validate_symptoms(
        symptoms
    )

    # If validation fails, stop the pipeline
    if not validation_result["valid"]:

        return {
            "input_symptoms": symptoms,
            "validation": validation_result,
            "predicted_condition": None,
            "model_confidence": None,
            "xai_explanation": None,
            "medicine_information": None
        }

    # Get validated symptoms
    valid_symptoms = validation_result[
        "valid_symptoms"
    ]

    # --------------------------------------------------------
    # STEP 2: DISEASE PREDICTION + XAI
    # --------------------------------------------------------

    prediction_result = predict_disease(
        valid_symptoms
    )

    predicted_condition = prediction_result[
        "condition"
    ]

    confidence = prediction_result[
        "confidence"
    ]

    # Get XAI explanation
    xai_explanation = prediction_result[
        "explanation"
    ]

    # --------------------------------------------------------
    # STEP 3: MEDICINE INFORMATION + SAFETY
    # --------------------------------------------------------

    medicine_result = get_medicine_with_safety(
        predicted_condition,
        max_results=3
    )

    # --------------------------------------------------------
    # STEP 4: RETURN COMPLETE RESULT
    # --------------------------------------------------------

    return {
        "input_symptoms": symptoms,
        "validation": validation_result,
        "predicted_condition": predicted_condition,
        "model_confidence": confidence,
        "xai_explanation": xai_explanation,
        "medicine_information": medicine_result
    }


# ============================================================
# TEST THE COMPLETE PIPELINE
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # TEST INPUT
    # --------------------------------------------------------

    test_symptoms = [
        "itching",
        "skin_rash"
    ]

    # --------------------------------------------------------
    # RUN PIPELINE
    # --------------------------------------------------------

    result = run_healthcare_pipeline(
        test_symptoms
    )

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    print("=" * 60)

    print(
        "HEALTHCARE DECISION-SUPPORT PIPELINE"
    )

    print("=" * 60)

    # ========================================================
    # VALIDATION RESULT
    # ========================================================

    print("\nValidation:")

    print(
        "Valid:",
        result["validation"]["valid"]
    )

    print(
        "Message:",
        result["validation"]["message"]
    )

    # --------------------------------------------------------
    # IF INPUT IS INVALID
    # --------------------------------------------------------

    if not result["validation"]["valid"]:

        print("\nInvalid symptoms:")

        for symptom in result[
            "validation"
        ]["invalid_symptoms"]:

            print(
                "-",
                symptom
            )

        print(
            "\nPipeline stopped because "
            "the input was invalid."
        )

    # --------------------------------------------------------
    # IF INPUT IS VALID
    # --------------------------------------------------------

    else:

        # ====================================================
        # INPUT SYMPTOMS
        # ====================================================

        print("\nInput symptoms:")

        for symptom in result[
            "input_symptoms"
        ]:

            print(
                "-",
                symptom
            )

        # ====================================================
        # PREDICTED CONDITION
        # ====================================================

        print("\nPredicted condition:")

        print(
            result["predicted_condition"]
        )

        # ====================================================
        # MODEL CONFIDENCE
        # ====================================================

        print("\nModel confidence:")

        print(
            f"{result['model_confidence'] * 100:.2f}%"
        )

        print(
            "\nNote: Model confidence is a probability "
            "estimate and not a medical diagnosis."
        )

        # ====================================================
        # XAI EXPLANATION
        # ====================================================

        print("\n" + "-" * 60)

        print(
            "XAI EXPLANATION"
        )

        print("-" * 60)

        xai = result[
            "xai_explanation"
        ]

        # ----------------------------------------------------
        # POSITIVE CONTRIBUTIONS
        # ----------------------------------------------------

        print("\nPositive contributions:")

        positive = xai[
            "positive_contributions"
        ]

        if positive:

            for item in positive:

                print(
                    f"- {item['symptom']}: "
                    f"{item['contribution']:.4f}"
                )

        else:

            print("None")

        # ----------------------------------------------------
        # NEGATIVE CONTRIBUTIONS
        # ----------------------------------------------------

        print("\nNegative contributions:")

        negative = xai[
            "negative_contributions"
        ]

        if negative:

            for item in negative:

                print(
                    f"- {item['symptom']}: "
                    f"{item['contribution']:.4f}"
                )

        else:

            print("None")

        print(
            "\nXAI Note: These contributions explain "
            "the model prediction."
        )

        print(
            "They do not prove medical causation "
            "or diagnosis."
        )

        # ====================================================
        # MEDICINE INFORMATION
        # ====================================================

        print("\n" + "-" * 60)

        print(
            "MEDICINE INFORMATION"
        )

        print("-" * 60)

        medicine_result = result[
            "medicine_information"
        ]

        print(
            "\nMedicine information found:"
        )

        print(
            medicine_result[
                "match_found"
            ]
        )

        print(
            "Number of medicines:",
            len(
                medicine_result[
                    "medicines"
                ]
            )
        )

        # ====================================================
        # DISPLAY EACH MEDICINE
        # ====================================================

        for index, medicine_result_item in enumerate(
            medicine_result["medicines"],
            start=1
        ):

            medicine = medicine_result_item[
                "medicine_information"
            ]

            safety = medicine_result_item[
                "safety"
            ]

            print("\n" + "-" * 60)

            print(
                f"Medicine {index}:"
            )

            print(
                medicine["name"]
            )

            print("\nUses:")

            print(
                medicine["uses"]
            )

            print("\nComposition:")

            print(
                medicine["composition"]
            )

            # ------------------------------------------------
            # SAFETY INFORMATION
            # ------------------------------------------------

            print(
                "\nSafety Information:"
            )

            for field, value in safety[
                "safety_information"
            ].items():

                print(
                    f"{field}: {value}"
                )

            # ------------------------------------------------
            # SAFETY WARNINGS
            # ------------------------------------------------

            print(
                "\nSafety warnings:"
            )

            if safety["warnings"]:

                for warning in safety[
                    "warnings"
                ]:

                    print(
                        "-",
                        warning
                    )

            else:

                print(
                    "No specific warnings found."
                )

        # ====================================================
        # FINAL SAFETY NOTICE
        # ====================================================

        print("\n" + "=" * 60)

        print(
            "IMPORTANT:"
        )

        print(
            "This system provides academic "
            "decision-support and medicine "
            "information only."
        )

        print(
            "It does not provide a medical diagnosis "
            "or prescribe medicines."
        )

        print(
            "Consult a qualified healthcare "
            "professional before making "
            "medical decisions."
        )

        print("=" * 60)