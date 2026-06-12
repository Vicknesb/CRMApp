import { useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useContact, useCreateContact, useUpdateContact } from "../hooks/useContacts";
import { Button } from "@/components/ui/Button";

const schema = z.object({
  firstName: z.string().min(1),
  lastName: z.string().min(1),
  email: z.string().email(),
  phone: z.string().optional(),
  title: z.string().optional(),
  department: z.string().optional(),
});

type FormValues = z.infer<typeof schema>;

export function ContactFormPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const isEdit = !!id;
  const { data: contact } = useContact(id ?? "");
  const createContact = useCreateContact();
  const updateContact = useUpdateContact();

  const { register, handleSubmit, reset, formState: { errors } } = useForm<FormValues>({
    resolver: zodResolver(schema),
  });

  useEffect(() => {
    if (contact) reset(contact);
  }, [contact, reset]);

  const onSubmit = async (values: FormValues) => {
    if (isEdit) {
      await updateContact.mutateAsync({ id: id!, body: values });
    } else {
      await createContact.mutateAsync(values);
    }
    navigate("/contacts");
  };

  return (
    <div className="max-w-lg">
      <h1 className="text-2xl font-bold mb-6">{isEdit ? "Edit" : "New"} Contact</h1>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div className="form-control">
            <label className="label"><span className="label-text">First Name</span></label>
            <input className="input input-bordered" {...register("firstName")} />
            {errors.firstName && <span className="text-error text-sm">{errors.firstName.message}</span>}
          </div>
          <div className="form-control">
            <label className="label"><span className="label-text">Last Name</span></label>
            <input className="input input-bordered" {...register("lastName")} />
            {errors.lastName && <span className="text-error text-sm">{errors.lastName.message}</span>}
          </div>
        </div>
        <div className="form-control">
          <label className="label"><span className="label-text">Email</span></label>
          <input className="input input-bordered" type="email" {...register("email")} />
          {errors.email && <span className="text-error text-sm">{errors.email.message}</span>}
        </div>
        <div className="form-control">
          <label className="label"><span className="label-text">Phone</span></label>
          <input className="input input-bordered" {...register("phone")} />
        </div>
        <div className="form-control">
          <label className="label"><span className="label-text">Title</span></label>
          <input className="input input-bordered" {...register("title")} />
        </div>
        <div className="form-control">
          <label className="label"><span className="label-text">Department</span></label>
          <input className="input input-bordered" {...register("department")} />
        </div>
        <div className="flex gap-3 pt-2">
          <Button type="submit" disabled={createContact.isPending || updateContact.isPending}>
            {isEdit ? "Save Changes" : "Create Contact"}
          </Button>
          <Button type="button" variant="ghost" onClick={() => navigate("/contacts")}>Cancel</Button>
        </div>
      </form>
    </div>
  );
}
