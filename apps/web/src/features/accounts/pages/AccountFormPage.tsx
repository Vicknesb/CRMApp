import { useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useAccount, useCreateAccount, useUpdateAccount } from "../hooks/useAccounts";
import { Button } from "@/components/ui/Button";

const schema = z.object({
  name: z.string().min(1),
  industry: z.string().optional(),
  type: z.string().optional(),
  website: z.string().url().optional().or(z.literal("")),
  phone: z.string().optional(),
  annualRevenue: z.coerce.number().optional(),
  employees: z.coerce.number().int().optional(),
});

type FormValues = z.infer<typeof schema>;

export function AccountFormPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const isEdit = !!id;
  const { data: account } = useAccount(id ?? "");
  const createAccount = useCreateAccount();
  const updateAccount = useUpdateAccount();

  const { register, handleSubmit, reset, formState: { errors } } = useForm<FormValues>({
    resolver: zodResolver(schema),
  });

  useEffect(() => {
    if (account) reset(account);
  }, [account, reset]);

  const onSubmit = async (values: FormValues) => {
    const payload = { ...values, website: values.website || undefined };
    if (isEdit) {
      await updateAccount.mutateAsync({ id: id!, body: payload });
    } else {
      await createAccount.mutateAsync(payload);
    }
    navigate("/accounts");
  };

  return (
    <div className="max-w-lg">
      <h1 className="text-2xl font-bold mb-6">{isEdit ? "Edit" : "New"} Account</h1>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div className="form-control">
          <label className="label"><span className="label-text">Name *</span></label>
          <input className="input input-bordered" {...register("name")} />
          {errors.name && <span className="text-error text-sm">{errors.name.message}</span>}
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div className="form-control">
            <label className="label"><span className="label-text">Industry</span></label>
            <input className="input input-bordered" {...register("industry")} />
          </div>
          <div className="form-control">
            <label className="label"><span className="label-text">Type</span></label>
            <input className="input input-bordered" {...register("type")} />
          </div>
        </div>
        <div className="form-control">
          <label className="label"><span className="label-text">Website</span></label>
          <input className="input input-bordered" type="url" {...register("website")} />
          {errors.website && <span className="text-error text-sm">{errors.website.message}</span>}
        </div>
        <div className="form-control">
          <label className="label"><span className="label-text">Phone</span></label>
          <input className="input input-bordered" {...register("phone")} />
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div className="form-control">
            <label className="label"><span className="label-text">Annual Revenue (₹)</span></label>
            <input className="input input-bordered" type="number" {...register("annualRevenue")} />
          </div>
          <div className="form-control">
            <label className="label"><span className="label-text">Employees</span></label>
            <input className="input input-bordered" type="number" {...register("employees")} />
          </div>
        </div>
        <div className="flex gap-3 pt-2">
          <Button type="submit" disabled={createAccount.isPending || updateAccount.isPending}>
            {isEdit ? "Save Changes" : "Create Account"}
          </Button>
          <Button type="button" variant="ghost" onClick={() => navigate("/accounts")}>Cancel</Button>
        </div>
      </form>
    </div>
  );
}
