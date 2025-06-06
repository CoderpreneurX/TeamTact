import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar,
} from "@/components/ui/sidebar";
import TeamTactIcon from "@/assets/favicon.svg";
import TeamTactLogo from "@/assets/teamtact-logo.png";
import type React from "react";
import { cn } from "@/lib/utils";
import { SidebarMenuItems } from "./SidebarLayout";
import { Link } from "react-router-dom";
import { NavUser } from "./nav-user";
import useUserStore from "@/store/UserStore";

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  const { open } = useSidebar();
  const user = useUserStore((state) => state.user)
  return (
    <Sidebar collapsible="icon" {...props}>
      <SidebarHeader className="mx-auto">
        <img
          src={!open ? TeamTactIcon : TeamTactLogo}
          className={cn("w-auto", open ? "h-10" : "h-8")}
          alt="TeamTact Logo"
        />
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarMenu>
            {SidebarMenuItems.navMain.map((item) => (
              <SidebarMenuItem key={item.title}>
                <SidebarMenuButton asChild>
                  <Link to={item.url}>
                    <item.icon />
                    <span className="font-semibold">{item.title}</span>
                  </Link>
                </SidebarMenuButton>
              </SidebarMenuItem>
            ))}
          </SidebarMenu>
        </SidebarGroup>
        <SidebarGroup />
        <SidebarGroup />
      </SidebarContent>
      <SidebarFooter>
        <NavUser user={user} />
      </SidebarFooter>
    </Sidebar>
  );
}
