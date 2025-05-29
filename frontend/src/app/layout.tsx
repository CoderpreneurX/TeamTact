import type { ReactNode } from "react";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/Sidebar/app-sidebar";

type MainLayoutProps = {
  children: ReactNode;
};

export const MainLayout = ({ children }: MainLayoutProps) => {
  return (
    <SidebarProvider>
      <div className="flex bg-gray-50 w-full h-screen">
        <AppSidebar />
        <main className="flex-1 p-4">
          <div className="mb-4 flex gap-x-4 items-center">
            <SidebarTrigger />
            <h1 className="font-bold text-2xl">My Teams</h1>
          </div>
          {children}
        </main>
      </div>
    </SidebarProvider>
  );
};