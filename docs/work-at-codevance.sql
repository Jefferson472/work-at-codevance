CREATE TABLE "CustomUser" (
  "id" [pk],
  "email" email
);

CREATE TABLE "BaseProfile" (
  "user" int,
  "name" varchar
);

CREATE TABLE "Suplier" (
  "id" [pk],
  "cnpj" varchar
);

CREATE TABLE "Operator" (
  "id" [pk]
);

CREATE TABLE "Payment" (
  "id" [pk],
  "suplier" int,
  "description" varchar,
  "value" int,
  "date_due" datetime,
  "is_active" boolean,
  "created" datetime
);

CREATE TABLE "AntecipationRequest" (
  "id" [pk],
  "payment" int,
  "requester" int,
  "request_date" datetime,
  "fee" int,
  "status" choices,
  "created" datetime,
  "updated" datetime
);

CREATE TABLE "Antecipation" (
  "id" [pk],
  "operator" int,
  "request_antecipation" int,
  "new_value" int,
  "created" datetime,
  "updated" datetime
);

CREATE TABLE "LogTransactions" (
  "id" [pk],
  "requester" int,
  "request_antecipation" int,
  "created" datetime,
  "transaction_type" choices,
  "status_after" choices,
  "value_before" int,
  "value_after" int
);

ALTER TABLE "BaseProfile" ADD FOREIGN KEY ("user") REFERENCES "CustomUser" ("id");

ALTER TABLE "Suplier" ADD FOREIGN KEY ("id") REFERENCES "BaseProfile" ("user");

ALTER TABLE "Operator" ADD FOREIGN KEY ("id") REFERENCES "BaseProfile" ("user");

ALTER TABLE "Payment" ADD FOREIGN KEY ("suplier") REFERENCES "Suplier" ("id");

ALTER TABLE "AntecipationRequest" ADD FOREIGN KEY ("payment") REFERENCES "Payment" ("id");

ALTER TABLE "AntecipationRequest" ADD FOREIGN KEY ("requester") REFERENCES "CustomUser" ("id");

ALTER TABLE "Antecipation" ADD FOREIGN KEY ("operator") REFERENCES "Operator" ("id");

ALTER TABLE "Antecipation" ADD FOREIGN KEY ("request_antecipation") REFERENCES "AntecipationRequest" ("id");

ALTER TABLE "LogTransactions" ADD FOREIGN KEY ("requester") REFERENCES "CustomUser" ("id");

ALTER TABLE "LogTransactions" ADD FOREIGN KEY ("request_antecipation") REFERENCES "AntecipationRequest" ("id");
