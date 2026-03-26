FROM python:3.12-slim

# Install basic system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    apt-utils \
    gcc \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create the user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /workspace

# Copy and install requirements (if they exist)
COPY . .

RUN pip install --upgrade pip && \
    if [ -f requirements.txt ]; then pip install -r requirements.txt; fi && \
    if [ -f dev-requirements.txt ]; then pip install -r dev-requirements.txt; fi

# Switch to non-root user
USER $USERNAME

CMD [ "bash" ]
