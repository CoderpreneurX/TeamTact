export const API_ROUTES = {
  AUTH: {
    LOGIN: "auth/login",
    REGISTER: "auth/signup",
    REFRESH_TOKEN: "auth/refresh",
    REQUEST_RESET_PASSWORD: "auth/request-reset-password",
    VALIDATE_RESET_PASSWORD_TOKEN: "auth/validate-reset-password-token",
    CONFIRM_RESET_PASSWORD: "auth/confirm-reset-password",
    VERIFY_EMAIL: "auth/verify-email",
    REQUEST_EMAIL_VERIFICATION: "auth/resend-verification-email",
    LOGOUT: "auth/logout",
  },
  TEAMS: {
    TEAMS: "teams/",
    AUTOGENERATE_TEAM_CODE: "teams/autogenerate-code",
    VALIDATE_TEAM_CODE: "teams/validate-code",
    GET_MEMBERS: "teams/:id/members",
    INVITE: "teams/invite",
  },
};

export const APP_ROUTES = {
  DASHBOARD: "/dashboard",
  TEAMS: "/teams",
  REQUEST_RESET_PASSWORD: "/request-reset-password",
  REQUEST_EMAIL_VERIFICATION: "/request-email-verification",
  LOGIN: "/login",
};

export const INTERNAL_SERVER_ERROR_MESSAGE = "Some Internal Server Error occurred, please try later!"