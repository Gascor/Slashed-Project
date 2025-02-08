#!/bin/bash

set -e  # Arrête le script en cas d'erreur

# Configuration
REPO_URL="github.com/Gascor/Slashed-Project.git"
PROJECT_DIR="/home/ubuntu/slashed-project"
DEPLOY_DIR="$PROJECT_DIR/slashed-project-website"
API_DB_DIR="$PROJECT_DIR/slashed-project-server"
GITHUB_TOKEN="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"

# Vérifiez si GITHUB_TOKEN est configuré
if [ -z "$GITHUB_TOKEN" ]; then
    echo "Erreur : GITHUB_TOKEN n'est pas défini."
    exit 1
fi

# Fonction pour installer les dépendances
install_dependencies() {
    echo "Installation des dépendances..."
    if ! command -v docker &> /dev/null; then
        curl -fsSL https://get.docker.com -o get-docker.sh
        sudo sh get-docker.sh
        sudo usermod -aG docker $USER
    fi

    if ! command -v docker-compose &> /dev/null; then
        sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose
    fi
}

# Fonction pour déployer le projet
deploy_project() {
    echo "Déploiement du projet..."
    if [ -d "$PROJECT_DIR" ]; then
        sudo rm -rf "$PROJECT_DIR"
    fi

    echo "Création du répertoire $PROJECT_DIR"
    mkdir -p "$PROJECT_DIR"

    echo "Clonage du dépôt dans $PROJECT_DIR"
    git clone "https://${GITHUB_TOKEN}@${REPO_URL}" "$PROJECT_DIR"
    cd "$DEPLOY_DIR"

    sudo docker-compose -f docker-compose.yml up --build -d
}

# Fonction pour mettre à jour le projet
update_project() {
    echo "Mise à jour du projet..."
    cd "$DEPLOY_DIR"
    git pull origin main
    sudo docker-compose -f docker-compose.yml up --build -d
}

# Fonction pour désinstaller le projet
uninstall_project() {
    echo "Désinstallation du projet..."
    cd "$DEPLOY_DIR"
    sudo docker-compose -f docker-compose.yml down
    sudo docker rmi $(sudo docker images 'slashed-project_web' -a -q)
    sudo docker volume prune -f
    sudo rm -rf $PROJECT_DIR
}

# Fonction pour vérifier l'état des services
check_status() {
    echo "Vérification de l'état des services..."
    cd "$DEPLOY_DIR"
    sudo docker-compose -f docker-compose.yml ps
}

# Fonction pour afficher les logs
view_logs() {
    echo "Affichage des logs..."
    cd "$DEPLOY_DIR"
    sudo docker-compose -f docker-compose.yml logs -f
}

# Fonction pour déployer l'API et la base de données
deploy_api_and_db() {
    echo "Déploiement de l'API et de la base de données..."
    if [ -d "$API_DB_DIR" ]; then
        sudo rm -rf "$API_DB_DIR"
    fi

    echo "Création du répertoire $API_DB_DIR"
    mkdir -p "$API_DB_DIR"

    echo "Clonage du dépôt dans $API_DB_DIR"
    git clone "https://${GITHUB_TOKEN}@${REPO_URL}" "$API_DB_DIR"
    cd "$API_DB_DIR"

    sudo docker-compose -f docker-compose.yml up --build -d
}

# Interface utilisateur
CHOICE=$(whiptail --title "Slashed Project Management" --menu "Choose an action" 15 60 7 \
"1" "Deploy Project" \
"2" "Update Project" \
"3" "Uninstall Project" \
"4" "Install Dependencies" \
"5" "Check Status" \
"6" "View Logs" \
"7" "Deploy API and Database" 3>&1 1>&2 2>&3)

case $CHOICE in
    1)
        install_dependencies
        deploy_project
        ;;
    2)
        install_dependencies
        update_project
        ;;
    3)
        uninstall_project
        ;;
    4)
        install_dependencies
        ;;
    5)
        check_status
        ;;
    6)
        view_logs
        ;;
    7)
        install_dependencies
        deploy_api_and_db
        ;;
esac

whiptail --title "Operation Completed" --msgbox "Selected operation ($CHOICE) has been completed successfully!" 8 78