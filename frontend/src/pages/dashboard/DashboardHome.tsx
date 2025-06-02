import { Users, LayoutDashboard } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Card } from "@/components/ui/card"

export function DashboardHome() {
  return (
    <div className="flex h-screen bg-muted/50">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r p-6 flex flex-col">
        <div className="text-2xl font-bold text-primary mb-10 flex items-center gap-2">
          <span className="text-purple-600">🌈</span> TeamTact
        </div>
        <nav className="space-y-2 text-sm font-medium">
          <a href="#" className="flex items-center gap-3 text-muted-foreground hover:text-primary">
            <LayoutDashboard className="w-4 h-4" /> Dashboard
          </a>
          <a href="#" className="flex items-center gap-3 text-muted-foreground hover:text-primary">
            <Users className="w-4 h-4" /> Teams
          </a>
        </nav>
      </aside>

      {/* Page content */}
      <main className="flex-1 overflow-y-auto p-8 space-y-6">
        {/* Page Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-semibold">My Teams</h1>
            <p className="text-muted-foreground text-sm">Manage and view your teams here.</p>
          </div>
          <Button variant="default">+ Create New</Button>
        </div>

        {/* Content Section */}
        <Card className="p-6 space-y-6">
          <div className="text-lg font-medium">Team Members</div>

          {/* Dummy table */}
          <div className="border rounded-md overflow-hidden">
            <div className="grid grid-cols-2 bg-muted px-4 py-2 font-medium text-muted-foreground text-sm">
              <div>Member</div>
              <div>Joined At</div>
            </div>

            <div className="grid grid-cols-2 items-center px-4 py-3 border-t hover:bg-muted/40 transition-colors">
              <div className="flex items-center gap-3">
                <Avatar className="h-8 w-8">
                  <AvatarFallback>PS</AvatarFallback>
                </Avatar>
                <div>
                  <p className="font-medium">Prabjeet Singh</p>
                  <p className="text-muted-foreground text-sm">prabjeet.jhass@gmail.com</p>
                </div>
              </div>
              <div className="text-sm text-muted-foreground">28/05/2025</div>
            </div>

            <div className="grid grid-cols-2 items-center px-4 py-3 border-t hover:bg-muted/40 transition-colors">
              <div className="flex items-center gap-3">
                <Avatar className="h-8 w-8">
                  <AvatarFallback>PK</AvatarFallback>
                </Avatar>
                <div>
                  <p className="font-medium">Prity Kapoor</p>
                  <p className="text-muted-foreground text-sm">prity.kapoor@gmail.com</p>
                </div>
              </div>
              <div className="text-sm text-muted-foreground">28/05/2025</div>
            </div>
          </div>
        </Card>
      </main>
    </div>
  )
}
