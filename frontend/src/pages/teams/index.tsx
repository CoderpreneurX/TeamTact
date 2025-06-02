import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { type ColumnDef } from "@tanstack/react-table";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Plus } from "lucide-react";
import { CreateTeamModal } from "./components/CreateTeamModal";
import { DataTable } from "@/components/ui/data-table";
import api from "@/utils/api";
import { API_ROUTES } from "@/utils/constants";
import { toast } from "sonner";

interface Team {
  id: string;
  name: string;
  code: string;
  createdAt: string;
}

export function TeamsPage() {
  const [teams, setTeams] = useState<Team[]>([]);
  const navigate = useNavigate();

  useEffect(() => {
    const getTeams = async () => {
      try {
        const response = await api.get(API_ROUTES.TEAMS.TEAMS);
        if (response.data?.success === true) {
          setTeams(response.data?.data);
        }
      } catch {
        toast.error("Couldn't load teams!");
      }
    };

    getTeams();
  }, []);

  const columns: ColumnDef<Team>[] = [
    {
      accessorKey: "name",
      header: "Name",
    },
    {
      accessorKey: "code",
      header: "Code",
    },
    {
      accessorKey: "createdAt",
      header: "Created At",
      cell: ({ getValue }) =>
        new Date(getValue() as string).toLocaleDateString(),
    },
    {
      id: "actions",
      header: "Actions",
      cell: ({ row }) => (
        <Button
          variant="link"
          className="p-0 h-auto"
          onClick={() => navigate(`/teams/${row.original.id}`)}
        >
          View
        </Button>
      ),
    },
  ];

  return (
    <div className="space-y-6 px-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">My Teams</h1>
        <CreateTeamModal
          trigger={
            <Button>
              <Plus className="mr-2 h-4 w-4" />
              Create New
            </Button>
          }
        />
      </div>

      {teams.length === 0 ? (
        <Card className="h-[400px] grid gap-2 justify-items-center place-content-center">
          <p className="text-lg font-medium">You don't have any teams yet!</p>
        </Card>
      ) : (
        <DataTable columns={columns} data={teams} />
      )}
    </div>
  );
}
