import type { ReactNode } from "react";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/Sidebar/app-sidebar";
import { useLocation } from "react-router-dom";
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";
import { Separator } from "@/components/ui/separator";
import { Home } from "lucide-react";

type MainLayoutProps = {
  children: ReactNode;
};

export const MainLayout = ({ children }: MainLayoutProps) => {
  const location = useLocation();
  const segments = location.pathname.split("/").filter(Boolean);

  // Function to capitalize and format segment names
  const formatSegmentName = (segment: string) => {
    return segment
      .split("-")
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(" ");
  };

  // Function to build the path up to a certain segment
  const buildPath = (index: number) => {
    const path = "/" + segments.slice(0, index + 1).join("/");
    return path;
  };

  return (
    <SidebarProvider>
      <div className="flex w-full h-screen">
        <AppSidebar />
        <main className="flex-1 overflow-y-auto">
          <div className="mb-4 flex flex-col gap-y-2">
            <header className="flex h-16 shrink-0 items-center gap-2 transition-[width,height] ease-linear group-has-data-[collapsible=icon]/sidebar-wrapper:h-12">
              <div className="flex items-center gap-2 px-4">
                <SidebarTrigger className="-ml-1" />
                <Separator
                  orientation="vertical"
                  className="mr-2 data-[orientation=vertical]:h-4"
                />
                <Breadcrumb>
                  <BreadcrumbList>
                    {segments.length > 0 ? (
                      <>
                        {/* Dynamic breadcrumbs for each segment */}
                        {segments.map((segment, index) => (
                          <div key={segment} className="flex items-center">
                            {index > 0 && <BreadcrumbSeparator className="hidden md:block" />}
                            <BreadcrumbItem className="hidden md:block">
                              {index === segments.length - 1 ? (
                                // Last segment as current page (not clickable)
                                <BreadcrumbPage className="font-medium">
                                  {formatSegmentName(segment)}
                                </BreadcrumbPage>
                              ) : (
                                // Intermediate segments as links
                                <BreadcrumbLink 
                                  to={buildPath(index)}
                                  className="transition-colors hover:text-foreground"
                                >
                                  {formatSegmentName(segment)}
                                </BreadcrumbLink>
                              )}
                            </BreadcrumbItem>
                          </div>
                        ))}
                      </>
                    ) : (
                      // Fallback for root path (though this shouldn't happen with your redirect)
                      <BreadcrumbItem>
                        <BreadcrumbLink 
                          to="/dashboard" 
                          className="flex items-center gap-1.5"
                        >
                          <Home className="h-4 w-4" />
                          <span className="sr-only md:not-sr-only">Dashboard</span>
                        </BreadcrumbLink>
                      </BreadcrumbItem>
                    )}
                  </BreadcrumbList>
                </Breadcrumb>
              </div>
            </header>
          </div>

          <div className="px-4 pb-4">
            {children}
          </div>
        </main>
      </div>
    </SidebarProvider>
  );
};