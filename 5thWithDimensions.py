import lcs
import moss

merge_git = """
void merge(vector<int>& arr, int left, int mid, int right) {
    int n1 = mid - left + 1;
    int n2 = right - mid;
    vector<int> L(n1), R(n2);

    for (int i = 0; i < n1; i++) L[i] = arr[left + i];
    for (int j = 0; j < n2; j++) R[j] = arr[mid + 1 + j];

    int i = 0, j = 0, k = left;
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k] = L[i]; i++;
        } else {
            arr[k] = R[j]; j++;
        }
        k++;
    }
    while (i < n1) { arr[k] = L[i]; i++; k++; }
    while (j < n2) { arr[k] = R[j]; j++; k++; }
}

void mergeSort(vector<int>& arr, int left, int right) {
    if (left >= right) return;
    int mid = left + (right - left) / 2;
    mergeSort(arr, left, mid);
    mergeSort(arr, mid + 1, right);
    merge(arr, left, mid, right);
}

"""

fake= """
void merge(vector<int>& arr, int left, int mid, int right) {
    
    int n1[1][1];
    int n2[1][1];

    n1[0][0] = mid - left + 1;
    n2[0][0] = right - mid;

    vector<vector<int>> L(1, vector<int>(n1[0][0]));
    vector<vector<int>> R(1, vector<int>(n2[0][0]));

    int i[1][1], j[1][1], k[1][1];

  
    for (i[0][0] = 0; i[0][0] < n1[0][0]; i[0][0]++) {
        L[0][i[0][0]] = arr[left + i[0][0]];
    }

    for (j[0][0] = 0; j[0][0] < n2[0][0]; j[0][0]++) {
        R[0][j[0][0]] = arr[mid + 1 + j[0][0]];
    }

    i[0][0] = 0;
    j[0][0] = 0;
    k[0][0] = left;

    while (i[0][0] < n1[0][0] && j[0][0] < n2[0][0]) {
        if (L[0][i[0][0]] <= R[0][j[0][0]]) {
            arr[k[0][0]] = L[0][i[0][0]];
            i[0][0]++;
        } else {
            arr[k[0][0]] = R[0][j[0][0]];
            j[0][0]++;
        }
        k[0][0]++;
    }

    while (i[0][0] < n1[0][0]) {
        arr[k[0][0]] = L[0][i[0][0]];
        i[0][0]++; k[0][0]++;
    }
    while (j[0][0] < n2[0][0]) {
        arr[k[0][0]] = R[0][j[0][0]];
        j[0][0]++; k[0][0]++;
    }
}

void mergeSort(vector<int>& arr, int left, int right) {
    if (left >= right) return;

    int mid[1][1];
    mid[0][0] = left + (right - left) / 2;

    mergeSort(arr, left, mid[0][0]);
    mergeSort(arr, mid[0][0] + 1, right);
    merge(arr, left, mid[0][0], right);
}
"""

mos = moss.MossDetector.compute_similarity(merge_git, fake, "cc")
print(mos)
ls = lcs.compute_lcs(merge_git, fake)
print(ls)