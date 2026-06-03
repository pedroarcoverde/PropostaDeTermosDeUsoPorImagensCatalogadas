# syntax=docker/dockerfile:1
FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /src

COPY ["ConsentTelemetry.csproj", "./"]
RUN dotnet restore "ConsentTelemetry.csproj"

COPY . .
RUN dotnet publish "ConsentTelemetry.csproj" -c Release -o /app/publish

FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS runtime
WORKDIR /app
COPY --from=build /app/publish .

ENV ASPNETCORE_URLS=http://+:8080
EXPOSE 8080
ENTRYPOINT ["dotnet", "ConsentTelemetry.dll"]
