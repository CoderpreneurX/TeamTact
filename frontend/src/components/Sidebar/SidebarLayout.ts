import { APP_ROUTES } from "@/utils/constants";
import { LayoutDashboard, Users } from "lucide-react";

export const SidebarMenuItems = {
    navMain: [
        {
            title: "Dashboard",
            url: APP_ROUTES.DASHBOARD,
            icon: LayoutDashboard,
        },
        {
            title: "Teams",
            url: APP_ROUTES.TEAMS,
            icon: Users,
        }
    ]
}