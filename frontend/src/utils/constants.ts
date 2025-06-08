export const API_ROUTES = {
  AUTH: {
    LOGIN: "auth/login",
    REGISTER: "auth/signup",
    REFRESH_TOKEN: "auth/refresh",
    REQUEST_RESET_PASSWORD: "auth/request-reset-password",
    VALIDATE_RESET_PASSWORD_TOKEN: "auth/validate-reset-password-token",
    CONFIRM_RESET_PASSWORD: "auth/confirm-reset-password",
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
  LOGIN: "/login"
};
