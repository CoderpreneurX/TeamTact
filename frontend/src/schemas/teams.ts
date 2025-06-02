import { z } from "zod";

export const createTeamSchema = z.object({
  name: z.string().min(3, "Team name should be at least 3 characters long!"),
  code: z.string().min(6, "Team code should be at least 6 characters long"),
});

export type CreateTeamFormValues = z.infer<typeof createTeamSchema>;