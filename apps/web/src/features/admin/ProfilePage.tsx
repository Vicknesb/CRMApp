import { useQuery, useMutation } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { apiClient } from "../../lib/apiClient";

const ProfileSchema = z.object({
  firstName: z.string().min(1),
  lastName: z.string().min(1),
  email: z.string().email(),
});

type ProfileForm = z.infer<typeof ProfileSchema>;

export function ProfilePage() {
  const profileQ = useQuery({
    queryKey: ["profile"],
    queryFn: () => apiClient.get("/auth/me").then(r => r.data),
  });

  const { register, handleSubmit, formState: { errors } } = useForm<ProfileForm>({
    resolver: zodResolver(ProfileSchema),
    values: profileQ.data ? {
      firstName: profileQ.data.firstName ?? "",
      lastName: profileQ.data.lastName ?? "",
      email: profileQ.data.email ?? "",
    } : undefined,
  });

  const update = useMutation({
    mutationFn: (data: ProfileForm) => apiClient.put("/auth/profile", data),
  });

  return (
    <div className="p-6 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">My Profile</h1>
      {profileQ.isLoading && <span className="loading loading-spinner" />}
      <div className="card bg-base-100 shadow">
        <div className="card-body">
          <form onSubmit={handleSubmit(d => update.mutate(d))} className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <div className="form-control">
                <label className="label"><span className="label-text">First Name</span></label>
                <input className="input input-bordered" {...register("firstName")} />
                {errors.firstName && <span className="text-error text-xs mt-1">{errors.firstName.message}</span>}
              </div>
              <div className="form-control">
                <label className="label"><span className="label-text">Last Name</span></label>
                <input className="input input-bordered" {...register("lastName")} />
              </div>
            </div>
            <div className="form-control">
              <label className="label"><span className="label-text">Email</span></label>
              <input className="input input-bordered" type="email" {...register("email")} />
            </div>
            <div className="flex items-center gap-4">
              <button className="btn btn-primary" type="submit" disabled={update.isPending}>
                {update.isPending ? <span className="loading loading-spinner loading-sm" /> : "Save Changes"}
              </button>
              {update.isSuccess && <span className="text-success text-sm">Saved!</span>}
            </div>
          </form>
        </div>
      </div>

      <div className="card bg-base-100 shadow mt-6">
        <div className="card-body">
          <h2 className="card-title">Role & Access</h2>
          <div className="flex gap-2 items-center">
            <span className="text-sm text-base-content/60">Role:</span>
            <span className="badge badge-outline">{profileQ.data?.role ?? "—"}</span>
          </div>
          <div className="flex gap-2 items-center">
            <span className="text-sm text-base-content/60">2FA:</span>
            <span className={`badge ${profileQ.data?.isTwoFactorEnabled ? "badge-success" : "badge-warning"}`}>
              {profileQ.data?.isTwoFactorEnabled ? "Enabled" : "Not configured"}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
