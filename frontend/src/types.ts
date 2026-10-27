export interface XAIContribution {
  symptom: string
  contribution: number
}

export interface XAIExplanation {
  positive_contributions: XAIContribution[]
  negative_contributions: XAIContribution[]
}

export interface MedicineDetails {
  name: string
  uses: string
  composition: string
  side_effects: string
  how_to_use: string
  alcohol: string
  pregnancy: string
  breast_feeding: string
  driving: string
  kidney: string
  liver: string
  manufacturer: string
}

export interface SafetyCheck {
  safety_available: boolean
  safety_information: {
    alcohol?: string
    pregnancy?: string
    breast_feeding?: string
    driving?: string
    kidney?: string
    liver?: string
    [key: string]: string | undefined
  }
  warnings: string[]
}

export interface MedicineRecord {
  medicine_information: MedicineDetails
  safety: SafetyCheck
}

export interface MedicineInformationResponse {
  condition: string
  match_found: boolean
  medicines: MedicineRecord[]
}

export interface PredictionSuccessResponse {
  input_symptoms: string[]
  predicted_condition: string
  model_confidence: number
  xai_explanation: XAIExplanation
  medicine_information: MedicineInformationResponse
  disclaimer: string
}

export interface ApiValidationErrorDetail {
  message: string
  invalid_symptoms: string[]
  validation?: {
    valid: boolean
    message: string
    valid_symptoms: string[]
    invalid_symptoms: string[]
  }
}

export type ApiErrorType = "validation" | "connection" | "server" | "client"

export interface ApiError {
  type: ApiErrorType
  message: string
  invalidSymptoms?: string[]
  statusCode?: number
}

// -------------------------------------------------------------
// PATIENT AUTHENTICATION & NOTIFICATION TYPES
// -------------------------------------------------------------

export interface PatientUser {
  id: number
  full_name: string
  email: string
  dob: string
  mobile: string
  age: number
  created_at: string
  status: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
  patient: PatientUser
}

export interface RegisterPayload {
  full_name: string
  dob: string
  mobile: string
  email: string
  password: string
  confirm_password: string
}

export interface LoginPayload {
  email: string
  password: string
}

export interface ResetPasswordPayload {
  email: string
  dob: string
  new_password: string
  confirm_password: string
}

export interface NotificationItem {
  id: string
  title: string
  message: string
  timestamp: string
  isRead: boolean
  type: "system" | "guidance" | "security"
}
