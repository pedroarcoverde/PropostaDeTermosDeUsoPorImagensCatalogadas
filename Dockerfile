# syntax=docker/dockerfile:1
ARG DOTNET_SDK_IMAGE=mcr.microsoft.com/dotnet/sdk:10.0
FROM ${DOTNET_SDK_IMAGE} AS build
WORKDIR /src
COPY . .
RUN dotnet restore
RUN dotnet publish -c Release -o /app/publish

ARG DOTNET_RUNTIME_IMAGE=mcr.microsoft.com/dotnet/aspnet:10.0
FROM ${DOTNET_RUNTIME_IMAGE} AS final
WORKDIR /app
COPY --from=build /app/publish .
ENV ASPNETCORE_URLS=http://+:8080
EXPOSE 8080
ENTRYPOINT ["dotnet","ConsentTelemetry.dll"]
# Build stage
FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /src

COPY ["ConsentTelemetry.csproj", "./"]
RUN dotnet restore "ConsentTelemetry.csproj"

COPY . .
RUN dotnet publish "ConsentTelemetry.csproj" -c Release -o /app/publish

# Runtime stage
FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS runtime
WORKDIR /app
COPY --from=build /app/publish .

ENV ASPNETCORE_URLS=http://+:80
EXPOSE 80

ENTRYPOINT ["dotnet", "ConsentTelemetry.dll"]
