import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { type ColumnDef } from "@tanstack/react-table";
import { DataTable } from "@/components/ui/data-table";
import { InviteUserModal } from "./components/InviteMemberModal"; // Adjust import path as needed
import api from "@/utils/api";
import { API_ROUTES } from "@/utils/constants";
import { toast } from "sonner";

interface Member {
  id: string;
  team_id: string;
  user_id: string;
  joined_at: string;
  team: {
    id: string;
    name: string;
  };
  user: {
    id: string;
    fullname: string;
    email: string;
    username: string;
    is_active: boolean;
    email_verified: boolean;
    created_at: string;
    updated_at: string;
  };
}

export function TeamViewPage() {
  const { id } = useParams();
  const [members, setMembers] = useState<Member[]>([]);
  const [teamNameFromAPI, setTeamNameFromAPI] = useState<string>("");

  useEffect(() => {
    const getTeamMembers = async () => {
      try {
        const response = await api.get(
          API_ROUTES.TEAMS.GET_MEMBERS.replace(":id", id as string)
        );

        if (response.data?.success) {
          const data = response.data.data;
          setMembers(data);
          if (data.length > 0) {
            setTeamNameFromAPI(data[0].team.name);
          }
        } else {
          toast.error(response.data?.message || "Failed to load team");
        }
      } catch {
        toast.error("Couldn't load team members!");
      }
    };

    getTeamMembers();
  }, [id]);

  const memberColumns: ColumnDef<Member>[] = [
    {
      id: "member",
      header: "Member",
      cell: ({ row }) => {
        const { fullname, email } = row.original.user;
        const initials = fullname
          .split(" ")
          .map((part) => part[0])
          .join("")
          .toUpperCase()
          .slice(0, 2);

        return (
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-full bg-primary text-white flex items-center justify-center text-sm font-semibold">
              {initials}
            </div>
            <div className="flex flex-col">
              <span className="font-medium">{fullname}</span>
              <span className="text-muted-foreground text-xs">{email}</span>
            </div>
          </div>
        );
      },
    },
    {
      accessorKey: "joined_at",
      header: "Joined At",
      cell: ({ getValue }) =>
        new Date(getValue() as string).toLocaleDateString(),
    },
  ];

  if (!members.length) return <p className="p-6">Loading team...</p>;

  return (
    <div className="space-y-6 px-2">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold mb-2">{teamNameFromAPI}</h1>
          <p className="text-sm text-muted-foreground">
            Total Members: {members.length}
          </p>
        </div>
        <InviteUserModal teamId={id as string} />
      </div>

      <div className="">
        <h2 className="text-xl font-semibold mb-4">Team Members</h2>
        <DataTable columns={memberColumns} data={members} />
      </div>
    </div>
  );
}