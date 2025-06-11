import { Loader2, LogOut } from "lucide-react";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar,
} from "@/components/ui/sidebar";
import type { User } from "@/store/UserStore";
import api from "@/utils/api";
import { API_ROUTES, INTERNAL_SERVER_ERROR_MESSAGE } from "@/utils/constants";
import { useNavigate } from "react-router-dom";
import { toast } from "sonner";
import { useState } from "react";

interface NavUserProps {
  user: User | null;
}

export function NavUser({ user }: NavUserProps) {
  const { isMobile } = useSidebar();
  const [isLoggingOut, setIsLoggingOut] = useState<boolean>(false)
  const navigate = useNavigate();

  const getInitials = (fullname: string | null) => {
    const [firstname = "", lastname = ""] = String(fullname).split(" ");
    return (
      firstname.charAt(0).toLocaleUpperCase() +
      (lastname.charAt(0)?.toLocaleUpperCase() ?? "")
    );
  };

  const initials = getInitials(user?.fullname ?? null);

  const handleLogout = async () => {
    setIsLoggingOut(true)
    try {
      const response = await api.get(API_ROUTES.AUTH.LOGOUT)

      if (response.data.success === true) {
        navigate("/login")
        toast.success(response.data.message)
      }
    } catch {
      toast.error(INTERNAL_SERVER_ERROR_MESSAGE)
    } finally {
      setIsLoggingOut(false)
    }
  }

  return (
    <SidebarMenu>
      <SidebarMenuItem>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <SidebarMenuButton
              size="lg"
              className="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground cursor-pointer border shadow-xs"
            >
              <Avatar className="h-8 w-8 rounded-lg">
                <AvatarImage src={""} alt={user?.fullname} />
                <AvatarFallback className="rounded-lg border font-semibold">
                  {initials}
                </AvatarFallback>
              </Avatar>
              <div className="grid flex-1 text-left text-sm leading-tight">
                <span className="truncate font-medium">{user?.fullname}</span>
                <span className="truncate text-xs">{user?.email}</span>
              </div>
            </SidebarMenuButton>
          </DropdownMenuTrigger>
          <DropdownMenuContent
            className="w-(--radix-dropdown-menu-trigger-width) min-w-56 rounded-lg"
            side={isMobile ? "bottom" : "right"}
            align="end"
            sideOffset={4}
          >
            <DropdownMenuLabel className="p-0 font-normal">
              <div className="flex items-center gap-2 px-1 py-1.5 text-left text-sm">
                <Avatar className="h-8 w-8 rounded-lg">
                  <AvatarImage src={""} alt={user?.fullname} />
                  <AvatarFallback className="rounded-lg border font-semibold">
                    {initials}
                  </AvatarFallback>
                </Avatar>
                <div className="grid flex-1 text-left text-sm leading-tight">
                  <span className="truncate font-medium">{user?.fullname}</span>
                  <span className="truncate text-xs">{user?.email}</span>
                </div>
              </div>
            </DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem onClick={handleLogout}>
              {isLoggingOut ? <Loader2 className="animate-spin"/> : <LogOut />}
              Log out
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </SidebarMenuItem>
    </SidebarMenu>
  );
}
