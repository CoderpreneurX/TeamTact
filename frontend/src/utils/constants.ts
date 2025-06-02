export const API_ROUTES = {
  AUTH: {
    LOGIN: "auth/login",
    REGISTER: "auth/signup",
    REFRESH_TOKEN: "auth/refresh",
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
};
