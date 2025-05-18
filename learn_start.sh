DIR='common'
FILE_LIST=`cat "${DIR}"/list.txt`
WRITE_FILE_NAME="${DIR}/name.py"
TAG=''
PROD_CHECK='test'
CORE='11'
PIPSERVER='100.95.241.19'

while getopts tsc-: opt; do
  OPTARG="${!OPTIND}"
  [[ "${opt}" = - ]] && opt="-${OPTARG}"
    
  case "${opt}" in
    s|-state)
      PROD_CHECK="${OPTARG}"
      shift
      ;;
    t|-tag)
      TAG="${OPTARG}"
      shift
      ;;
    c|-core)
      CORE="${OPTARG}"
      shift
      ;;
  esac
done

if [ -z "${TAG}" ]; then
  echo '1: name update'
  echo '2: data update and learn'
  echo '3: learn'
  echo '4: optuna learn'
  echo '5: simulation'
  
  read -p "Enter 1,2,3,4,5 > " TAG
fi

if [ !"${TAG}" = '1' ] && [ !"${TAG}" = '2' ] && [ !"${TAG}" = '3' ] && [ !"${TAG}" = '4' ] && [ !"${TAG}" = '5' ]; then
  echo "Wrong number"
  exit 1
fi

pip install --extra-index-url http://"${PIPSERVER}" --trusted-host "${PIPSERVER}" -U SekitobaLibrary

BASE='        self.'
rm -rf "${WRITE_FILE_NAME}"
echo 'class Name:' >> "${WRITE_FILE_NAME}"
echo '    def __init__( self ):' >> "${WRITE_FILE_NAME}"

for FILE_NAME in ${FILE_LIST}; do
  ARR=(${FILE_NAME//./ })
  NAME=${ARR[0]}
  echo "${BASE}${NAME} = \"${NAME}\"" >> "${WRITE_FILE_NAME}"
done

cp -r "${DIR}" data_analyze/
cp -r "${DIR}" learn/

PYTHON_COMMAND='python main.py'

if [ "${TAG}" = '2' ]; then
  mpiexec -n 10 ${PYTHON_COMMAND} -u True
  mpiexec -n "${CORE}" ${PYTHON_COMMAND} -l True -s "${PROD_CHECK}"
fi

if [ "${TAG}" = '3' ]; then
  mpiexec -n "${CORE}" ${PYTHON_COMMAND} -l True -s "${PROD_CHECK}"
fi

if [ "${TAG}" = '4' ]; then
  ${PYTHON_COMMAND} -o True -s "${PROD_CHECK}"
fi

if [ "${TAG}" = '5' ]; then
  ${PYTHON_COMMAND} -b True
fi

rm -rf storage
